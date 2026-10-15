import os
import sys
from datetime import datetime, timedelta, timezone

import pytest

# The backend imports modules by bare name ("import db"), so put backend/ on the path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import EmailDeliveryError  # noqa: E402
from verification import InMemoryVerificationStore, VerificationService  # noqa: E402


# Clock we can move forward by hand in tests
class FakeClock:
    def __init__(self):
        self.t = datetime(2026, 10, 14, 12, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.t

    def advance(self, **kwargs):
        self.t += timedelta(**kwargs)


# Fake sender that saves messages instead of sending, can be set to fail
class CapturingSender:
    def __init__(self):
        self.messages = []
        self.fail = False

    def send(self, message):
        if self.fail:
            raise EmailDeliveryError("simulated outage")
        self.messages.append(message)

    def last_code(self):
        # The subject is "<code> is your LionLift verification code".
        return self.messages[-1]["Subject"].split()[0]


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def sender():
    return CapturingSender()


@pytest.fixture
def store():
    return InMemoryVerificationStore()


@pytest.fixture
def service(store, sender, clock):
    return VerificationService(
        store=store,
        sender=sender,
        secret=b"test-secret",
        from_address="LionLift <no-reply@lionlift.local>",
        now=clock,
    )
