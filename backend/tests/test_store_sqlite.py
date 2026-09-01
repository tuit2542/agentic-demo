from __future__ import annotations

import os
import tempfile

import pytest

from src.models import ClickRecord
from src.store_sqlite import SqliteStore


@pytest.fixture
def sqlite_store():
    """Create a temporary SQLite store for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    store = SqliteStore(db_path)
    yield store
    store.close()
    os.unlink(db_path)


def test_shorten_returns_short_id(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    assert isinstance(sid, str)
    assert len(sid) == 6


def test_resolve_returns_original_url(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    assert sqlite_store.resolve(sid) == "https://example.com"


def test_resolve_unknown_returns_none(sqlite_store):
    assert sqlite_store.resolve("zzzzzz") is None


def test_click_count_increments(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    sqlite_store.resolve(sid)
    sqlite_store.resolve(sid)
    assert sqlite_store.stats(sid) == 2


def test_stats_unknown_returns_zero(sqlite_store):
    assert sqlite_store.stats("zzzzzz") == 0


def test_record_click_returns_click_record(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    record = sqlite_store.record_click(sid)
    assert isinstance(record, ClickRecord)
    assert record.timestamp is not None
    assert record.referrer is None


def test_get_history_returns_clicks(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    sqlite_store.resolve(sid)
    sqlite_store.resolve(sid)
    history = sqlite_store.get_history(sid)
    assert len(history) == 2
    assert isinstance(history[0], ClickRecord)


def test_get_history_unknown_returns_empty_list(sqlite_store):
    assert sqlite_store.get_history("zzzzzz") == []


# === Edge Cases ===


def test_duplicate_urls_get_different_short_ids(sqlite_store):
    sid1 = sqlite_store.shorten("https://example.com")
    sid2 = sqlite_store.shorten("https://example.com")
    assert sid1 != sid2
    assert sqlite_store.resolve(sid1) == "https://example.com"
    assert sqlite_store.resolve(sid2) == "https://example.com"


def test_short_id_is_alphanumeric(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    assert sid.isalnum()


def test_record_click_with_referrer(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    record = sqlite_store.record_click(sid, referrer="https://google.com")
    assert record.referrer == "https://google.com"


def test_stats_increments_after_resolve(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    assert sqlite_store.stats(sid) == 0
    sqlite_store.resolve(sid)
    assert sqlite_store.stats(sid) == 1
    sqlite_store.resolve(sid)
    assert sqlite_store.stats(sid) == 2


def test_history_preserves_order(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    sqlite_store.record_click(sid, referrer="https://a.com")
    sqlite_store.record_click(sid, referrer="https://b.com")
    sqlite_store.record_click(sid, referrer="https://c.com")
    history = sqlite_store.get_history(sid)
    assert len(history) == 3
    assert history[0].referrer == "https://a.com"
    assert history[1].referrer == "https://b.com"
    assert history[2].referrer == "https://c.com"


def test_resolve_returns_same_url(sqlite_store):
    sid = sqlite_store.shorten("https://example.com")
    result = sqlite_store.resolve(sid)
    assert result is not None
    assert result == "https://example.com"


def test_empty_url_accepted(sqlite_store):
    sid = sqlite_store.shorten("")
    assert sqlite_store.resolve(sid) == ""


def test_long_url_accepted(sqlite_store):
    long_url = "https://example.com/" + "a" * 2000
    sid = sqlite_store.shorten(long_url)
    assert sqlite_store.resolve(sid) == long_url


# === Persistence Tests ===


def test_persistence_across_instances():
    """Test that data persists across SqliteStore instances."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        # First instance
        store1 = SqliteStore(db_path)
        sid = store1.shorten("https://example.com")
        store1.resolve(sid)
        store1.close()

        # Second instance - should see the data (resolve adds 1 more click)
        store2 = SqliteStore(db_path)
        try:
            assert store2.resolve(sid) == "https://example.com"
            assert store2.stats(sid) == 2
            history = store2.get_history(sid)
            assert len(history) == 2
        finally:
            store2.close()
    finally:
        for suffix in ["", "-wal", "-shm"]:
            p = db_path + suffix
            if os.path.exists(p):
                try:
                    os.unlink(p)
                except PermissionError:
                    pass


def test_persistence_stats_and_history():
    """Test stats and history persist."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        store1 = SqliteStore(db_path)
        sid = store1.shorten("https://example.com")
        store1.record_click(sid, referrer="https://google.com")
        store1.record_click(sid, referrer="https://bing.com")
        store1.close()

        store2 = SqliteStore(db_path)
        assert store2.stats(sid) == 2
        history = store2.get_history(sid)
        assert len(history) == 2
        assert history[0].referrer == "https://google.com"
        assert history[1].referrer == "https://bing.com"
        store2.close()
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_concurrent_instances_same_data():
    """Test two instances can read same data."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        store1 = SqliteStore(db_path)
        sid = store1.shorten("https://example.com")
        store1.close()

        store2 = SqliteStore(db_path)
        store3 = SqliteStore(db_path)

        assert store2.resolve(sid) == "https://example.com"
        assert store3.resolve(sid) == "https://example.com"

        store2.close()
        store3.close()
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
