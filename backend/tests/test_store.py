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
