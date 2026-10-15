import pytest
from flask import Flask

from routes.auth import auth_bp


@pytest.fixture
def client(service):
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.extensions["verification_service"] = service
    return app.test_client()


def test_full_flow(client, sender):
    r = client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    assert r.status_code == 202
    assert r.get_json() == {"status": "sent", "email": "abc123@psu.edu", "expires_in": 600, "resend_after": 60}

    r = client.post("/api/auth/verify", json={"email": "abc123@psu.edu", "code": sender.last_code()})
    assert r.status_code == 200
    assert r.get_json() == {"verified": True, "email": "abc123@psu.edu"}


def test_rejects_non_psu_email(client):
    r = client.post("/api/auth/request-code", json={"email": "a@gmail.com"})
    assert r.status_code == 400
    assert r.get_json()["error"] == "invalid_email"


@pytest.mark.parametrize("path", ["/api/auth/request-code", "/api/auth/verify"])
@pytest.mark.parametrize("kwargs", [{"data": "not json"}, {"json": ["a", "list"]}, {}])
def test_rejects_bad_bodies(client, path, kwargs):
    r = client.post(path, **kwargs)
    assert r.status_code == 400
    assert r.get_json()["error"] == "invalid_request"


def test_rate_limit_sets_retry_after(client):
    client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    r = client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    assert r.status_code == 429
    assert r.headers["Retry-After"] == "60"
    assert r.get_json()["retry_after"] == 60


def test_wrong_code_then_lockout(client, sender):
    client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    wrong = f"{(int(sender.last_code()) + 1) % 10**6:06d}"
    for remaining in (4, 3, 2, 1):
        r = client.post("/api/auth/verify", json={"email": "abc123@psu.edu", "code": wrong})
        assert r.status_code == 400
        assert r.get_json()["attempts_remaining"] == remaining
    r = client.post("/api/auth/verify", json={"email": "abc123@psu.edu", "code": wrong})
    assert r.status_code == 429
    assert r.get_json()["error"] == "too_many_attempts"


def test_bad_code_format(client):
    client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    r = client.post("/api/auth/verify", json={"email": "abc123@psu.edu", "code": "12ab"})
    assert r.status_code == 400
    assert r.get_json()["error"] == "invalid_code_format"


def test_delivery_failure_is_503(client, sender):
    sender.fail = True
    r = client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    assert r.status_code == 503
    assert r.get_json()["error"] == "delivery_failed"


def test_real_app_module_starts_with_defaults(monkeypatch, capsys):
    # app.py with no environment set: in-memory store and console emails.
    for key in ("VERIFICATION_STORE", "EMAIL_BACKEND", "VERIFICATION_SECRET"):
        monkeypatch.delenv(key, raising=False)
    import importlib
    import app as app_module
    importlib.reload(app_module)
    client = app_module.app.test_client()

    r = client.post("/api/auth/request-code", json={"email": "abc123@psu.edu"})
    assert r.status_code == 202
    printed = capsys.readouterr().out
    assert "To: abc123@psu.edu" in printed
    code = printed.split("verification code is: ")[1][:6]

    r = client.post("/api/auth/verify", json={"email": "abc123@psu.edu", "code": code})
    assert r.get_json() == {"verified": True, "email": "abc123@psu.edu"}
