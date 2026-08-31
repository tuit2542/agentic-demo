from __future__ import annotations

from src.models import ClickRecord
from src.store import UrlStore


def test_shorten_returns_short_id():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert isinstance(sid, str)
    assert len(sid) == 6


def test_resolve_returns_original_url():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert store.resolve(sid) == "https://example.com"


def test_resolve_unknown_returns_none():
    store = UrlStore()
    assert store.resolve("zzzzzz") is None


def test_click_count_increments():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    store.resolve(sid)
    store.resolve(sid)
    assert store.stats(sid) == 2


def test_stats_unknown_returns_zero():
    store = UrlStore()
    assert store.stats("zzzzzz") == 0


def test_record_click_returns_click_record():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    record = store.record_click(sid)
    assert isinstance(record, ClickRecord)
    assert record.timestamp is not None
    assert record.referrer is None


def test_get_history_returns_clicks():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    store.resolve(sid)
    store.resolve(sid)
    history = store.get_history(sid)
    assert len(history) == 2
    assert isinstance(history[0], ClickRecord)


def test_get_history_unknown_returns_empty_list():
    store = UrlStore()
    assert store.get_history("zzzzzz") == []


# === Edge Cases ===


def test_duplicate_urls_get_different_short_ids():
    store = UrlStore()
    sid1 = store.shorten("https://example.com")
    sid2 = store.shorten("https://example.com")
    assert sid1 != sid2
    assert store.resolve(sid1) == "https://example.com"
    assert store.resolve(sid2) == "https://example.com"


def test_short_id_is_alphanumeric():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert sid.isalnum()


def test_record_click_with_referrer():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    record = store.record_click(sid, referrer="https://google.com")
    assert record.referrer == "https://google.com"


def test_stats_increments_after_resolve():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert store.stats(sid) == 0
    store.resolve(sid)
    assert store.stats(sid) == 1
    store.resolve(sid)
    assert store.stats(sid) == 2


def test_history_preserves_order():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    store.record_click(sid, referrer="https://a.com")
    store.record_click(sid, referrer="https://b.com")
    store.record_click(sid, referrer="https://c.com")
    history = store.get_history(sid)
    assert len(history) == 3
    assert history[0].referrer == "https://a.com"
    assert history[1].referrer == "https://b.com"
    assert history[2].referrer == "https://c.com"


def test_resolve_returns_same_url():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    result = store.resolve(sid)
    assert result is not None
    assert result == "https://example.com"


def test_empty_url_accepted():
    store = UrlStore()
    sid = store.shorten("")
    assert store.resolve(sid) == ""


def test_long_url_accepted():
    store = UrlStore()
    long_url = "https://example.com/" + "a" * 2000
    sid = store.shorten(long_url)
    assert store.resolve(sid) == long_url
