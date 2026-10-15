import socket

import pytest

from email_sender import (
    ConsoleEmailSender,
    EmailDeliveryError,
    SmtpEmailSender,
    build_sender_from_env,
    build_verification_email,
)


def _message():
    return build_verification_email(
        to="abc123@psu.edu", from_address="LionLift <rides@example.com>", code="042917", ttl_minutes=10
    )


def test_message_contents():
    m = _message()
    assert m["Subject"] == "042917 is your LionLift verification code"
    assert m["To"] == "abc123@psu.edu"
    assert m["Message-ID"].endswith("@example.com>")
    plain = m.get_body(("plain",)).get_content()
    assert "042917" in plain and "10 minutes" in plain
    assert "042917" in m.get_body(("html",)).get_content()


def test_console_sender_prints(capsys):
    ConsoleEmailSender().send(_message())
    out = capsys.readouterr().out
    assert "To: abc123@psu.edu" in out and "042917" in out


def test_env_selection():
    assert isinstance(build_sender_from_env({}), ConsoleEmailSender)
    s = build_sender_from_env({
        "EMAIL_BACKEND": "smtp", "SMTP_HOST": "smtp.gmail.com",
        "SMTP_USERNAME": "u@gmail.com", "SMTP_PASSWORD": "app-password",
    })
    assert isinstance(s, SmtpEmailSender)
    assert (s.port, s.security) == (587, "starttls")
    with pytest.raises(ValueError, match="SMTP_PASSWORD"):
        build_sender_from_env({"EMAIL_BACKEND": "smtp", "SMTP_HOST": "h", "SMTP_USERNAME": "u"})
    with pytest.raises(ValueError):
        build_sender_from_env({"EMAIL_BACKEND": "pigeon"})


def test_unreachable_server_raises_delivery_error():
    # Port 9 on localhost has nothing listening, so the connection is refused.
    with pytest.raises(EmailDeliveryError):
        SmtpEmailSender(host="127.0.0.1", port=9, security="none", timeout=2).send(_message())


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_real_smtp_round_trip():
    # Send through a real SMTP server running in this process.
    aiosmtpd = pytest.importorskip("aiosmtpd.controller")
    from aiosmtpd.handlers import Message

    received = []

    class Collect(Message):
        def handle_message(self, message):
            received.append(message)

    port = _free_port()
    controller = aiosmtpd.Controller(Collect(), hostname="127.0.0.1", port=port)
    controller.start()
    try:
        SmtpEmailSender(host="127.0.0.1", port=port, security="none").send(_message())
    finally:
        controller.stop()

    assert len(received) == 1
    got = received[0]
    assert got["To"] == "abc123@psu.edu"
    assert got["Subject"] == "042917 is your LionLift verification code"
