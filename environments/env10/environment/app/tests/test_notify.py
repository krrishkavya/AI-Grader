import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_database
from notify_filter import filter_messages, list_channels, channel_stats

@pytest.fixture(autouse=True)
def setup_db():
    init_database()

def test_filter_messages():
    messages = filter_messages("user101")
    assert len(messages) == 3

def test_list_channels():
    chans = list_channels()
    assert "email" in chans
    assert "sms" in chans
    assert "push" in chans

def test_channel_stats():
    stats = channel_stats()
    assert stats["email"] >= 2
    assert stats["sms"] >= 2
