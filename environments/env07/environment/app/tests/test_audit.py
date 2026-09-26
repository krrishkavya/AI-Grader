import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_database
from audit_viewer import query_events, query_summary, query_recent

@pytest.fixture(autouse=True)
def setup_db():
    init_database()

def test_query_events():
    events = query_events("LOGIN")
    assert len(events) == 2
    users = [e["user"] for e in events]
    assert "alice" in users
    assert "bob" in users

def test_query_summary():
    summary = query_summary()
    assert "INFO" in summary
    assert "WARN" in summary
    assert "HIGH" in summary

def test_query_recent():
    recent = query_recent(limit=3)
    assert len(recent) == 3
