"""
Penn State email verification (issue #12).

Flow
----
1. The app POSTs an email to /api/auth/request-code.
2. We check it is a Penn State address, generate a random 6-digit code,
   store only a keyed hash of it, and email the code to the address.
3. The user types the code into the app, which POSTs it to /api/auth/verify.
4. If the code matches, is not expired, and the attempt limit has not been
   reached, the address is marked verified (verified_at is set).

Security parameters (see VerificationConfig for the values)
-----------------------------------------------------------
Let N = 10**code_length (number of possible codes), k = max_attempts
(guesses allowed per code) and m = max_sends_per_window (codes that can be
issued for one address per window).

A code is drawn uniformly from {0, ..., N-1} with the `secrets` CSPRNG.
Someone who does not have access to the inbox and makes j distinct guesses
against one code succeeds with probability exactly j/N, so at most k/N per
code. Over one window at most m codes exist, so by the union bound

    P(success in one window) <= m * k / N

With the defaults (N = 10**6, k = 5, m = 5, window = 1 hour) that is
2.5e-5 per address per hour.

Codes are stored as HMAC-SHA256(secret, email || 0x00 || code). A plain hash
would be useless: with only 10**6 possible codes, anyone who reads the table
could try all of them in well under a second. With the secret key, the table
alone does not reveal the code.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import math
import os
import re
import secrets
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from typing import Callable, ContextManager, Iterator, Optional, Protocol

from email_sender import EmailDeliveryError, EmailSender, build_verification_email

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Email address validation
# --------------------------------------------------------------------------

DEFAULT_ALLOWED_DOMAINS = ("psu.edu",)

# RFC 5322 "dot-atom" local part: atoms of allowed characters joined by single
# dots, with no leading, trailing, or consecutive dots.
_ATOM = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
_LOCAL_PART = re.compile(rf"^{_ATOM}(?:\.{_ATOM})*$")

MAX_LOCAL_PART_LENGTH = 64  # RFC 5321, section 4.5.3.1.1
MAX_ADDRESS_LENGTH = 254  # RFC 5321 path limit minus the angle brackets


class InvalidEmail(ValueError):
    pass


def normalize_psu_email(raw: object, allowed_domains=DEFAULT_ALLOWED_DOMAINS) -> str:
    """Return the address lowercased and trimmed, or raise InvalidEmail.

    The address is accepted only if all of these hold:
      * it has exactly one "@",
      * the domain is exactly one of `allowed_domains` (so "x@psu.edu" passes
        but "x@cse.psu.edu" and "x@psu.edu.evil.com" do not),
      * the local part is a valid dot-atom of at most 64 characters,
      * the whole address is at most 254 characters.
    """
    if not isinstance(raw, str):
        raise InvalidEmail("Email must be a string.")
    email = raw.strip().lower()
    if len(email) > MAX_ADDRESS_LENGTH:
        raise InvalidEmail("Email is too long.")
    if email.count("@") != 1:
        raise InvalidEmail("Enter a valid email address.")
    local, domain = email.split("@")
    if domain not in allowed_domains:
        allowed = ", ".join("@" + d for d in allowed_domains)
        raise InvalidEmail(f"Use your Penn State email ({allowed}).")
    if not local or len(local) > MAX_LOCAL_PART_LENGTH or not _LOCAL_PART.match(local):
        raise InvalidEmail("Enter a valid email address.")
    return email


# --------------------------------------------------------------------------
# Configuration and stored state
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class VerificationConfig:
    code_length: int = 6
    code_ttl: timedelta = timedelta(minutes=10)
    max_attempts: int = 5  # wrong guesses allowed per code
    resend_cooldown: timedelta = timedelta(seconds=60)
    max_sends_per_window: int = 5
    send_window: timedelta = timedelta(hours=1)
    allowed_domains: tuple = DEFAULT_ALLOWED_DOMAINS


@dataclass
class VerificationRecord:
    """One row per email address."""
    email: str
    code_hash: Optional[str] = None  # None means there is no pending code
    expires_at: Optional[datetime] = None
    attempts: int = 0
    last_sent_at: Optional[datetime] = None
    window_start: Optional[datetime] = None
    sends_in_window: int = 0
    verified_at: Optional[datetime] = None

    def clear_code(self) -> None:
        self.code_hash = None
        self.expires_at = None
        self.attempts = 0


class VerificationStore(Protocol):
    def locked(self, email: str) -> ContextManager[VerificationRecord]:
        """Yield the record for `email`, creating an empty one if needed.

        Nobody else can change that record until the block exits. Changes
        are saved if the block exits normally and thrown away if it raises,
        so the service decides the outcome inside the block and raises only
        after it has exited.
        """

    def get(self, email: str) -> Optional[VerificationRecord]:
        ...


class InMemoryVerificationStore:
    """Keeps records in a dict. Used for local development and tests.
    Everything is lost when the server restarts."""

    def __init__(self) -> None:
        self._records: dict[str, VerificationRecord] = {}
        self._lock = threading.Lock()

    @contextmanager
    def locked(self, email: str) -> Iterator[VerificationRecord]:
        with self._lock:
            record = replace(self._records.get(email) or VerificationRecord(email))
            yield record  # if the block raises, the copy is simply dropped
            self._records[email] = record

    def get(self, email: str) -> Optional[VerificationRecord]:
        with self._lock:
            record = self._records.get(email)
            return replace(record) if record else None


# --------------------------------------------------------------------------
# Errors the routes turn into HTTP responses
# --------------------------------------------------------------------------

class VerificationError(Exception):
    code = "verification_error"


class RateLimited(VerificationError):
    code = "rate_limited"

    def __init__(self, retry_after: int):
        super().__init__(f"Too many codes requested. Try again in {retry_after} seconds.")
        self.retry_after = retry_after


class DeliveryFailed(VerificationError):
    code = "delivery_failed"


class InvalidCodeFormat(VerificationError):
    code = "invalid_code_format"


class NoPendingCode(VerificationError):
    code = "no_pending_code"


class CodeExpired(VerificationError):
    code = "code_expired"


class IncorrectCode(VerificationError):
    code = "incorrect_code"

    def __init__(self, attempts_remaining: int):
        super().__init__(f"Incorrect code. {attempts_remaining} attempt(s) left.")
        self.attempts_remaining = attempts_remaining


class TooManyAttempts(VerificationError):
    code = "too_many_attempts"


@dataclass(frozen=True)
class CodeSent:
    email: str
    expires_in: int  # seconds
    resend_after: int  # seconds


# --------------------------------------------------------------------------
# Service
# --------------------------------------------------------------------------

def _ceil_seconds(delta: timedelta) -> int:
    return max(1, math.ceil(delta.total_seconds()))


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class VerificationService:
    store: VerificationStore
    sender: EmailSender
    secret: bytes
    from_address: str
    config: VerificationConfig = field(default_factory=VerificationConfig)
    now: Callable[[], datetime] = _utc_now

    def _hash(self, email: str, code: str) -> str:
        message = email.encode() + b"\x00" + code.encode()
        return hmac.new(self.secret, message, hashlib.sha256).hexdigest()

    def _new_code(self) -> str:
        n = self.config.code_length
        return f"{secrets.randbelow(10 ** n):0{n}d}"

    def request_code(self, raw_email: object) -> CodeSent:
        """Issue a new code for the address and email it (issue #18).

        A new code replaces any earlier one and resets its attempt counter.
        That reset does not weaken the bound in the module docstring, because
        the number of codes per window is itself limited.
        """
        cfg = self.config
        email = normalize_psu_email(raw_email, cfg.allowed_domains)
        t = self.now()

        limited: Optional[RateLimited] = None
        with self.store.locked(email) as r:
            if r.window_start is None or t - r.window_start >= cfg.send_window:
                r.window_start, r.sends_in_window = t, 0
            if r.last_sent_at is not None and t - r.last_sent_at < cfg.resend_cooldown:
                limited = RateLimited(_ceil_seconds(r.last_sent_at + cfg.resend_cooldown - t))
            elif r.sends_in_window >= cfg.max_sends_per_window:
                limited = RateLimited(_ceil_seconds(r.window_start + cfg.send_window - t))
            else:
                code = self._new_code()
                r.code_hash = self._hash(email, code)
                r.expires_at = t + cfg.code_ttl
                r.attempts = 0
                r.last_sent_at = t
                # Counted before sending, so a failed send still uses up one
                # of the m sends. That keeps the bound true even if sending fails.
                r.sends_in_window += 1
        if limited is not None:
            raise limited

        message = build_verification_email(
            to=email,
            from_address=self.from_address,
            code=code,
            ttl_minutes=_ceil_seconds(cfg.code_ttl) // 60,
        )
        try:
            self.sender.send(message)
        except EmailDeliveryError as exc:
            log.error("Could not send verification email to %s: %s", email, exc)
            raise DeliveryFailed("We couldn't send the email. Try again shortly.") from exc

        return CodeSent(
            email=email,
            expires_in=_ceil_seconds(cfg.code_ttl),
            resend_after=_ceil_seconds(cfg.resend_cooldown),
        )

    def verify(self, raw_email: object, raw_code: object) -> str:
        """Check a code. Returns the normalized email on success, raises otherwise."""
        cfg = self.config
        email = normalize_psu_email(raw_email, cfg.allowed_domains)
        code = raw_code.strip() if isinstance(raw_code, str) else ""
        if not re.fullmatch(rf"\d{{{cfg.code_length}}}", code):
            # Malformed input is rejected without using an attempt. It could
            # never match, so the bound above is unaffected.
            raise InvalidCodeFormat(f"The code is {cfg.code_length} digits.")
        t = self.now()

        # Decide the outcome while holding the lock, then raise after the
        # block exits. That way the attempt counter is always saved.
        outcome: Optional[VerificationError] = None
        with self.store.locked(email) as r:
            if r.code_hash is None:
                outcome = NoPendingCode("No active code for this email. Request a new one.")
            elif t >= r.expires_at:
                r.clear_code()
                outcome = CodeExpired("This code has expired. Request a new one.")
            else:
                r.attempts += 1
                if hmac.compare_digest(r.code_hash, self._hash(email, code)):
                    r.clear_code()  # a code works only once
                    r.verified_at = t
                elif r.attempts >= cfg.max_attempts:
                    r.clear_code()
                    outcome = TooManyAttempts("Too many incorrect attempts. Request a new code.")
                else:
                    outcome = IncorrectCode(cfg.max_attempts - r.attempts)

        if outcome is not None:
            raise outcome
        return email

    def is_verified(self, raw_email: object) -> bool:
        """For the sign-up endpoint: has this address completed verification?"""
        try:
            email = normalize_psu_email(raw_email, self.config.allowed_domains)
        except InvalidEmail:
            return False
        record = self.store.get(email)
        return record is not None and record.verified_at is not None


# --------------------------------------------------------------------------
# Building the service from environment variables (see backend/.env.example)
# --------------------------------------------------------------------------

def build_service_from_env(env=os.environ) -> VerificationService:
    from email_sender import build_sender_from_env

    secret = env.get("VERIFICATION_SECRET")
    if not secret:
        log.warning(
            "VERIFICATION_SECRET is not set; using a random key. "
            "Codes issued before a restart will stop working."
        )
        secret_bytes = secrets.token_bytes(32)
    else:
        secret_bytes = secret.encode()

    domains = tuple(
        d.strip().lower()
        for d in env.get("ALLOWED_EMAIL_DOMAINS", ",".join(DEFAULT_ALLOWED_DOMAINS)).split(",")
        if d.strip()
    )

    store_kind = env.get("VERIFICATION_STORE", "memory").lower()
    if store_kind == "postgres":
        from verification_store_pg import PostgresVerificationStore
        store = PostgresVerificationStore()
    elif store_kind == "memory":
        store = InMemoryVerificationStore()
    else:
        raise ValueError(f"VERIFICATION_STORE must be 'memory' or 'postgres', not {store_kind!r}")

    return VerificationService(
        store=store,
        sender=build_sender_from_env(env),
        secret=secret_bytes,
        from_address=env.get("EMAIL_FROM", "LionLift <no-reply@lionlift.local>"),
        config=VerificationConfig(allowed_domains=domains),
    )
