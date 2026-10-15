# Backend

Flask API for LionLift. **Use a virtual environment to run it locally.**

## Setup

From the `backend` folder:

```sh
python -m venv .venv
.venv\Scripts\activate        # Windows (PowerShell)
source .venv/bin/activate     # macOS / Linux
pip install -r requirements-dev.txt
```

Optionally copy `.env.example` to `.env` and fill it in. With no `.env`, everything still works: codes are kept in memory and emails are printed in the terminal.

## Run

```sh
python -m flask --app app run --debug
```

The server runs at http://127.0.0.1:5000. Run it from inside `backend/`, because the modules import each other by name (`import db`).

## Test

```sh
python -m pytest -q
```

The Postgres store tests are skipped unless `TEST_DATABASE_URL` is set, for example `postgresql://postgres:password@127.0.0.1:5432/postgres`. **Warning:** they drop and recreate the `email_verifications` table in that database.

## Email verification API (issue #12)

Only Penn State addresses (`@psu.edu`) can sign up. The app asks for a code, the user receives it by email, and the app sends it back.

### `POST /api/auth/request-code`

```json
{ "email": "abc123@psu.edu" }
```

| Status | Body |
|---|---|
| 202 | `{"status": "sent", "email": "abc123@psu.edu", "expires_in": 600, "resend_after": 60}` |
| 400 | `{"error": "invalid_email", "message": "..."}`: not a valid `@psu.edu` address |
| 429 | `{"error": "rate_limited", "retry_after": 42, ...}`, plus a `Retry-After` header |
| 503 | `{"error": "delivery_failed", ...}`: the email could not be sent |

### `POST /api/auth/verify`

```json
{ "email": "abc123@psu.edu", "code": "123456" }
```

| Status | Body |
|---|---|
| 200 | `{"verified": true, "email": "abc123@psu.edu"}` |
| 400 | `error` is one of: `invalid_email`, `invalid_code_format`, `no_pending_code`, `code_expired`, or `incorrect_code` (which includes `attempts_remaining`) |
| 429 | `{"error": "too_many_attempts", ...}`: the code is now dead and a new one is needed |

Every error includes a `message` the app can show to the user directly.

### Rules

| Rule | Value |
|---|---|
| Code | 6 digits, drawn uniformly at random with Python's `secrets` |
| Expires | 10 minutes after it is sent; works only once |
| Wrong guesses | 5 per code, then the code is invalidated |
| Resend cooldown | 60 seconds |
| Codes per address | 5 per hour |

With N = 10^6 possible codes, k = 5 guesses per code and m = 5 codes per hour, someone without access to the inbox succeeds with probability at most m·k/N = 2.5 × 10⁻⁵ per address per hour. `verification.py` explains the derivation. Codes are stored only as HMAC-SHA256 hashes keyed with `VERIFICATION_SECRET`.

The future sign-up endpoint should call `verification_service.is_verified(email)` before creating the user.

### Files

- `verification.py`: email validation, code issuing and checking, in-memory store
- `verification_store_pg.py`: Postgres store (`VERIFICATION_STORE=postgres`)
- `email_sender.py`: verification email content, console sender and SMTP sender (issue #18)
- `routes/auth.py`: the two endpoints above
- `docs/email-service.md`: which email provider to use and how to set it up (issue #17)

### Trying it from PowerShell

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/auth/request-code `
  -ContentType "application/json" -Body '{"email": "abc123@psu.edu"}'
# copy the code printed in the server terminal, then:
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/auth/verify `
  -ContentType "application/json" -Body '{"email": "abc123@psu.edu", "code": "123456"}'
```
