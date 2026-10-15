"""
Sending email (issue #18).

Two senders:
  * ConsoleEmailSender prints the email to the server terminal. It is the
    default, so you can test sign-up without any email account.
  * SmtpEmailSender sends real email through any SMTP server. Gmail, Brevo,
    Mailgun and Resend all offer SMTP, so switching providers only means
    changing environment variables (see backend/docs/email-service.md, #17).
"""

from __future__ import annotations

import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import make_msgid, parseaddr
from typing import Protocol

log = logging.getLogger(__name__)


class EmailDeliveryError(Exception):
    pass


class EmailSender(Protocol):
    def send(self, message: EmailMessage) -> None:
        """Send the message, or raise EmailDeliveryError."""


def build_verification_email(to: str, from_address: str, code: str, ttl_minutes: int) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = f"{code} is your LionLift verification code"
    message["From"] = from_address
    message["To"] = to
    sender_domain = parseaddr(from_address)[1].rpartition("@")[2]
    message["Message-ID"] = make_msgid(domain=sender_domain or None)

    message.set_content(
        f"Your LionLift verification code is: {code}\n"
        f"\n"
        f"It expires in {ttl_minutes} minutes and can only be used once.\n"
        f"\n"
        f"If you didn't try to sign up for LionLift, you can ignore this email.\n"
        f"\n"
        f"LionLift - ride sharing for the Penn State Abington community\n"
    )
    message.add_alternative(
        f"""\
<!doctype html>
<html>
  <body style="margin:0;padding:24px;background:#F4F6FA;font-family:Arial,Helvetica,sans-serif;color:#1A1A1A;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
      <tr><td align="center">
        <table role="presentation" width="420" cellspacing="0" cellpadding="0"
               style="max-width:420px;background:#FFFFFF;border-radius:12px;padding:32px;">
          <tr><td style="font-size:20px;font-weight:bold;color:#1E407C;">LionLift</td></tr>
          <tr><td style="padding-top:16px;font-size:15px;">Your verification code is:</td></tr>
          <tr><td style="padding:16px 0;font-size:34px;font-weight:bold;letter-spacing:8px;color:#1E407C;">{code}</td></tr>
          <tr><td style="font-size:14px;color:#4A4A4A;">
            It expires in {ttl_minutes} minutes and can only be used once.<br><br>
            If you didn't try to sign up for LionLift, you can ignore this email.
          </td></tr>
        </table>
        <p style="font-size:12px;color:#6B6B6B;">Ride sharing for the Penn State Abington community</p>
      </td></tr>
    </table>
  </body>
</html>
""",
        subtype="html",
    )
    return message


class ConsoleEmailSender:
    """Prints emails instead of sending them. Development only."""

    def send(self, message: EmailMessage) -> None:
        body = message.get_body(preferencelist=("plain",))
        text = body.get_content() if body is not None else ""
        print(
            "\n----- EMAIL (console backend, not actually sent) -----\n"
            f"To: {message['To']}\nFrom: {message['From']}\nSubject: {message['Subject']}\n\n"
            f"{text}"
            "------------------------------------------------------\n",
            flush=True,
        )


@dataclass
class SmtpEmailSender:
    host: str
    port: int
    username: str = ""
    password: str = ""
    security: str = "starttls"  # "starttls" (port 587), "ssl" (port 465), or "none" (local test servers)
    timeout: float = 15.0

    def __post_init__(self) -> None:
        if self.security not in ("starttls", "ssl", "none"):
            raise ValueError("SMTP security must be 'starttls', 'ssl' or 'none'")

    def send(self, message: EmailMessage) -> None:
        context = ssl.create_default_context()
        try:
            if self.security == "ssl":
                client = smtplib.SMTP_SSL(self.host, self.port, timeout=self.timeout, context=context)
            else:
                client = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            with client:
                if self.security == "starttls":
                    client.starttls(context=context)
                if self.username:
                    client.login(self.username, self.password)
                client.send_message(message)
        except (smtplib.SMTPException, OSError) as exc:
            raise EmailDeliveryError(f"{type(exc).__name__}: {exc}") from exc


def build_sender_from_env(env) -> EmailSender:
    kind = env.get("EMAIL_BACKEND", "console").lower()
    if kind == "console":
        return ConsoleEmailSender()
    if kind == "smtp":
        missing = [k for k in ("SMTP_HOST", "SMTP_USERNAME", "SMTP_PASSWORD") if not env.get(k)]
        if missing:
            raise ValueError(f"EMAIL_BACKEND=smtp needs these environment variables: {', '.join(missing)}")
        return SmtpEmailSender(
            host=env["SMTP_HOST"],
            port=int(env.get("SMTP_PORT", "587")),
            username=env["SMTP_USERNAME"],
            password=env["SMTP_PASSWORD"],
            security=env.get("SMTP_SECURITY", "starttls").lower(),
        )
    raise ValueError(f"EMAIL_BACKEND must be 'console' or 'smtp', not {kind!r}")
