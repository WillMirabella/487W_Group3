# Runs the Postgres store against a real database. Skipped unless
# TEST_DATABASE_URL is set, for example:
#
# TEST_DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/postgres
#
# WARNING: drops and recreates the email_verifications table in that database.

import os
import threading

import pytest

psycopg2 = pytest.importorskip("psycopg2")
DSN = os.environ.get("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DSN, reason="TEST_DATABASE_URL not set")


@pytest.fixture
def pg_store():
    from verification_store_pg import PostgresVerificationStore

    conn = psycopg2.connect(DSN)
    with conn, conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS email_verifications")
    conn.close()
    return PostgresVerificationStore(connect=lambda: psycopg2.connect(DSN))


@pytest.fixture
def pg_service(pg_store, sender, clock):
    from verification import VerificationService
    return VerificationService(
        store=pg_store, sender=sender, secret=b"test-secret",
        from_address="LionLift <no-reply@lionlift.local>", now=clock,
    )


def test_round_trip(pg_service, pg_store, sender):
    pg_service.request_code("abc123@psu.edu")
    record = pg_store.get("abc123@psu.edu")
    assert len(record.code_hash) == 64 and record.sends_in_window == 1
    assert record.expires_at.tzinfo is not None
    assert pg_service.verify("abc123@psu.edu", sender.last_code())
    assert pg_service.is_verified("abc123@psu.edu")
    assert pg_store.get("abc123@psu.edu").code_hash is None


def test_attempts_persist_across_calls(pg_service, pg_store, sender):
    from verification import IncorrectCode, TooManyAttempts
    pg_service.request_code("abc123@psu.edu")
    wrong = f"{(int(sender.last_code()) + 1) % 10**6:06d}"
    for remaining in (4, 3, 2, 1):
        with pytest.raises(IncorrectCode) as info:
            pg_service.verify("abc123@psu.edu", wrong)
        assert info.value.attempts_remaining == remaining
        assert pg_store.get("abc123@psu.edu").attempts == 5 - remaining
    with pytest.raises(TooManyAttempts):
        pg_service.verify("abc123@psu.edu", wrong)


def test_concurrent_guesses_cannot_exceed_limit(pg_service, sender):
    # 20 threads guess wrong at the same time, the row lock should make them go one at a time
    # so 4 get IncorrectCode, 1 gets TooManyAttempts, and the other 15 find no code left
    from verification import IncorrectCode, NoPendingCode, TooManyAttempts
    pg_service.request_code("abc123@psu.edu")
    wrong = f"{(int(sender.last_code()) + 1) % 10**6:06d}"

    results = []
    lock = threading.Lock()
    start = threading.Barrier(20)

    def guess():
        start.wait()
        try:
            pg_service.verify("abc123@psu.edu", wrong)
            outcome = "ok"
        except (IncorrectCode, TooManyAttempts, NoPendingCode) as exc:
            outcome = type(exc).__name__
        with lock:
            results.append(outcome)

    threads = [threading.Thread(target=guess) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert results.count("IncorrectCode") == 4
    assert results.count("TooManyAttempts") == 1
    assert results.count("NoPendingCode") == 15
