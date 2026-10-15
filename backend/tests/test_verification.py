import re

import pytest

from verification import (
    CodeExpired,
    DeliveryFailed,
    IncorrectCode,
    InvalidCodeFormat,
    InvalidEmail,
    NoPendingCode,
    RateLimited,
    TooManyAttempts,
    normalize_psu_email,
)


# ---------------------------------------------------------------- validation

@pytest.mark.parametrize("raw, expected", [
    ("abc123@psu.edu", "abc123@psu.edu"),
    ("  ABC123@PSU.EDU ", "abc123@psu.edu"),
    ("first.last@psu.edu", "first.last@psu.edu"),
    ("abc+rides@psu.edu", "abc+rides@psu.edu"),
])
def test_accepts_psu_addresses(raw, expected):
    assert normalize_psu_email(raw) == expected


@pytest.mark.parametrize("raw", [
    None, 123, "", "abc123", "abc123@gmail.com", "abc123@cse.psu.edu",
    "abc123@psu.edu.evil.com", "abc@123@psu.edu", "@psu.edu", ".abc@psu.edu",
    "abc.@psu.edu", "a..b@psu.edu", "a b@psu.edu", "a" * 65 + "@psu.edu",
])
def test_rejects_other_addresses(raw):
    with pytest.raises(InvalidEmail):
        normalize_psu_email(raw)


def test_allowed_domains_are_configurable():
    assert normalize_psu_email("x@cse.psu.edu", ("psu.edu", "cse.psu.edu")) == "x@cse.psu.edu"


# ---------------------------------------------------------------- happy path

def test_request_then_verify(service, sender, store):
    sent = service.request_code("ABC123@psu.edu")
    assert sent.email == "abc123@psu.edu"
    assert (sent.expires_in, sent.resend_after) == (600, 60)

    assert len(sender.messages) == 1
    message = sender.messages[0]
    code = sender.last_code()
    assert re.fullmatch(r"\d{6}", code)
    assert message["To"] == "abc123@psu.edu"
    assert code in message.get_body(("plain",)).get_content()
    assert code in message.get_body(("html",)).get_content()

    # Only the keyed hash is stored, never the code.
    record = store.get("abc123@psu.edu")
    assert record.code_hash is not None and code not in record.code_hash
    assert not service.is_verified("abc123@psu.edu")

    assert service.verify("abc123@psu.edu", f" {code} ") == "abc123@psu.edu"
    assert service.is_verified("ABC123@PSU.EDU")


def test_code_works_only_once(service, sender):
    service.request_code("abc123@psu.edu")
    code = sender.last_code()
    service.verify("abc123@psu.edu", code)
    with pytest.raises(NoPendingCode):
        service.verify("abc123@psu.edu", code)


def test_codes_are_bound_to_their_email(service, sender, clock):
    service.request_code("aaa111@psu.edu")
    code_a = sender.last_code()
    service.request_code("bbb222@psu.edu")
    code_b = sender.last_code()
    if code_a == code_b:  # 1-in-a-million collision; the test would be meaningless
        pytest.skip("random codes collided")
    with pytest.raises(IncorrectCode):
        service.verify("bbb222@psu.edu", code_a)


# ---------------------------------------------------------------- guessing

def test_wrong_codes_count_down_then_lock(service, sender):
    service.request_code("abc123@psu.edu")
    right = sender.last_code()
    wrong = f"{(int(right) + 1) % 10**6:06d}"

    for remaining in (4, 3, 2, 1):
        with pytest.raises(IncorrectCode) as info:
            service.verify("abc123@psu.edu", wrong)
        assert info.value.attempts_remaining == remaining

    with pytest.raises(TooManyAttempts):
        service.verify("abc123@psu.edu", wrong)
    # The 5th wrong guess killed the code, so even the right one fails now.
    with pytest.raises(NoPendingCode):
        service.verify("abc123@psu.edu", right)


def test_correct_code_on_last_attempt_succeeds(service, sender):
    service.request_code("abc123@psu.edu")
    right = sender.last_code()
    wrong = f"{(int(right) + 1) % 10**6:06d}"
    for _ in range(4):
        with pytest.raises(IncorrectCode):
            service.verify("abc123@psu.edu", wrong)
    assert service.verify("abc123@psu.edu", right)


@pytest.mark.parametrize("bad", ["12345", "1234567", "abcdef", "", None, 123456])
def test_malformed_codes_do_not_use_attempts(service, sender, bad):
    service.request_code("abc123@psu.edu")
    for _ in range(10):
        with pytest.raises(InvalidCodeFormat):
            service.verify("abc123@psu.edu", bad)
    assert service.verify("abc123@psu.edu", sender.last_code())


def test_verify_without_request(service):
    with pytest.raises(NoPendingCode):
        service.verify("abc123@psu.edu", "123456")


# ---------------------------------------------------------------- expiry

def test_code_expires_after_ten_minutes(service, sender, clock):
    service.request_code("abc123@psu.edu")
    code = sender.last_code()
    clock.advance(minutes=10)  # expires_at is exclusive: t >= expires_at is expired
    with pytest.raises(CodeExpired):
        service.verify("abc123@psu.edu", code)
    with pytest.raises(NoPendingCode):
        service.verify("abc123@psu.edu", code)


def test_code_valid_just_before_expiry(service, sender, clock):
    service.request_code("abc123@psu.edu")
    clock.advance(minutes=9, seconds=59)
    assert service.verify("abc123@psu.edu", sender.last_code())


# ---------------------------------------------------------------- send limits

def test_resend_cooldown(service, clock):
    service.request_code("abc123@psu.edu")
    clock.advance(seconds=20)
    with pytest.raises(RateLimited) as info:
        service.request_code("abc123@psu.edu")
    assert info.value.retry_after == 40
    clock.advance(seconds=40)
    service.request_code("abc123@psu.edu")


def test_new_code_replaces_old_and_resets_attempts(service, sender, clock):
    service.request_code("abc123@psu.edu")
    old = sender.last_code()
    wrong = f"{(int(old) + 1) % 10**6:06d}"
    for _ in range(3):
        with pytest.raises(IncorrectCode):
            service.verify("abc123@psu.edu", wrong)

    clock.advance(seconds=60)
    service.request_code("abc123@psu.edu")
    new = sender.last_code()
    if new != old:
        with pytest.raises(IncorrectCode) as info:
            service.verify("abc123@psu.edu", old)
        assert info.value.attempts_remaining == 4
    assert service.verify("abc123@psu.edu", new)


def test_at_most_five_codes_per_hour(service, clock):
    for _ in range(5):
        service.request_code("abc123@psu.edu")
        clock.advance(seconds=60)
    # 5 sends at t = 0, 60, ..., 240 s; now t = 300 s, window opened at t = 0.
    with pytest.raises(RateLimited) as info:
        service.request_code("abc123@psu.edu")
    assert info.value.retry_after == 3600 - 300
    clock.advance(seconds=3300)  # t = 3600 s: a new window starts
    service.request_code("abc123@psu.edu")


def test_limits_are_per_address(service):
    service.request_code("aaa111@psu.edu")
    service.request_code("bbb222@psu.edu")  # not blocked by aaa111's cooldown


def test_rate_limited_request_keeps_existing_code(service, sender, clock):
    service.request_code("abc123@psu.edu")
    code = sender.last_code()
    clock.advance(seconds=5)
    with pytest.raises(RateLimited):
        service.request_code("abc123@psu.edu")
    assert service.verify("abc123@psu.edu", code)


# ---------------------------------------------------------------- delivery

def test_failed_send_raises_and_still_counts(service, sender, clock):
    sender.fail = True
    with pytest.raises(DeliveryFailed):
        service.request_code("abc123@psu.edu")
    # The failed attempt used the cooldown, so it can't be used to spam retries.
    with pytest.raises(RateLimited):
        service.request_code("abc123@psu.edu")
    sender.fail = False
    clock.advance(seconds=60)
    service.request_code("abc123@psu.edu")
    assert service.verify("abc123@psu.edu", sender.last_code())


def test_invalid_email_sends_nothing(service, sender):
    with pytest.raises(InvalidEmail):
        service.request_code("someone@gmail.com")
    assert sender.messages == []


# ---------------------------------------------------------------- randomness

def test_codes_are_zero_padded_and_spread_out(service, sender, clock):
    """Sanity check on the generator over many draws (not a proof of uniformity):
    every code is exactly 6 digits, and leading digits 0-9 all appear."""
    leading = set()
    for i in range(400):
        service.request_code(f"u{i}@psu.edu")
        code = sender.last_code()
        assert re.fullmatch(r"\d{6}", code)
        leading.add(code[0])
    # P(a given digit never leads in 400 draws) = 0.9**400 ~ 5e-19.
    assert leading == set("0123456789")
