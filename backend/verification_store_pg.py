# Postgres storage for verification records (issue #12)
# Uses the email_verifications table from db.py, turn on with VERIFICATION_STORE=postgres

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterator, Optional

import db
from verification import VerificationRecord

_COLUMNS = (
    "email, code_hash, expires_at, attempts, last_sent_at, "
    "window_start, sends_in_window, verified_at"
)


def _row_to_record(row) -> VerificationRecord:
    return VerificationRecord(*row)


class PostgresVerificationStore:
    def __init__(self, connect: Callable = db.get_connection, ensure_schema: bool = True):
        self._connect = connect
        if ensure_schema:
            with self._connection() as conn, conn.cursor() as cur:
                cur.execute(db.EMAIL_VERIFICATIONS_DDL)
                conn.commit()

    @contextmanager
    def _connection(self):
        conn = self._connect()
        if not conn:  # db.get_connection() returns False when it can't connect
            raise RuntimeError("Could not connect to PostgreSQL (see db.get_connection).")
        try:
            yield conn
        finally:
            conn.close()

    # Locks the row with SELECT ... FOR UPDATE so two requests for the same email
    # run one after the other (stops people getting extra guesses by sending at once)
    @contextmanager
    def locked(self, email: str) -> Iterator[VerificationRecord]:
        with self._connection() as conn:
            try:
                with conn.cursor() as cur:
                    # make sure the row exists so there's something to lock
                    cur.execute(
                        "INSERT INTO email_verifications (email) VALUES (%s) "
                        "ON CONFLICT (email) DO NOTHING",
                        (email,),
                    )
                    cur.execute(
                        f"SELECT {_COLUMNS} FROM email_verifications WHERE email = %s FOR UPDATE",
                        (email,),
                    )
                    record = _row_to_record(cur.fetchone())
                    try:
                        yield record
                    finally:
                        cur.execute(
                            """
                            UPDATE email_verifications
                            SET code_hash = %s, expires_at = %s, attempts = %s,
                                last_sent_at = %s, window_start = %s,
                                sends_in_window = %s, verified_at = %s
                            WHERE email = %s
                            """,
                            (
                                record.code_hash, record.expires_at, record.attempts,
                                record.last_sent_at, record.window_start,
                                record.sends_in_window, record.verified_at, email,
                            ),
                        )
                conn.commit()
            except BaseException:
                conn.rollback()
                raise

    def get(self, email: str) -> Optional[VerificationRecord]:
        with self._connection() as conn, conn.cursor() as cur:
            cur.execute(f"SELECT {_COLUMNS} FROM email_verifications WHERE email = %s", (email,))
            row = cur.fetchone()
            return _row_to_record(row) if row else None
