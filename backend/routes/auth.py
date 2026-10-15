"""
Email verification API (issue #12).

POST /api/auth/request-code   {"email": "abc123@psu.edu"}
POST /api/auth/verify         {"email": "abc123@psu.edu", "code": "123456"}

Every error response has the shape {"error": <machine code>, "message": <text to show the user>}.
"""

from flask import Blueprint, current_app, jsonify, request

from verification import (
    CodeExpired,
    DeliveryFailed,
    IncorrectCode,
    InvalidCodeFormat,
    InvalidEmail,
    NoPendingCode,
    RateLimited,
    TooManyAttempts,
    VerificationService,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _service() -> VerificationService:
    return current_app.extensions["verification_service"]


def _error(status: int, code: str, message: str, **extra):
    return jsonify({"error": code, "message": message, **extra}), status


def _json_body():
    body = request.get_json(silent=True)
    return body if isinstance(body, dict) else None


@auth_bp.post("/request-code")
def request_code():
    body = _json_body()
    if body is None:
        return _error(400, "invalid_request", 'Send JSON like {"email": "abc123@psu.edu"}.')
    try:
        sent = _service().request_code(body.get("email"))
    except InvalidEmail as exc:
        return _error(400, "invalid_email", str(exc))
    except RateLimited as exc:
        response, status = _error(429, exc.code, str(exc), retry_after=exc.retry_after)
        response.headers["Retry-After"] = str(exc.retry_after)
        return response, status
    except DeliveryFailed as exc:
        return _error(503, exc.code, str(exc))

    return jsonify({
        "status": "sent",
        "email": sent.email,
        "expires_in": sent.expires_in,
        "resend_after": sent.resend_after,
    }), 202


@auth_bp.post("/verify")
def verify():
    body = _json_body()
    if body is None:
        return _error(400, "invalid_request", 'Send JSON like {"email": "...", "code": "123456"}.')
    try:
        email = _service().verify(body.get("email"), body.get("code"))
    except InvalidEmail as exc:
        return _error(400, "invalid_email", str(exc))
    except IncorrectCode as exc:
        return _error(400, exc.code, str(exc), attempts_remaining=exc.attempts_remaining)
    except (InvalidCodeFormat, NoPendingCode, CodeExpired) as exc:
        return _error(400, exc.code, str(exc))
    except TooManyAttempts as exc:
        return _error(429, exc.code, str(exc))

    return jsonify({"verified": True, "email": email}), 200
