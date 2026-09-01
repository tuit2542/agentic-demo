from __future__ import annotations

import time

from src.rate_limiter import RateLimiter, get_rate_limiter


def test_check_allows_within_limit():
    limiter = RateLimiter(limit=5, window=60)
    for _ in range(5):
        assert limiter.check("key1") is True


def test_check_blocks_after_limit():
    limiter = RateLimiter(limit=3, window=60)
    assert limiter.check("key1") is True
    assert limiter.check("key1") is True
    assert limiter.check("key1") is True
    assert limiter.check("key1") is False


def test_check_resets_after_window():
    limiter = RateLimiter(limit=2, window=1)
    assert limiter.check("key1") is True
    assert limiter.check("key1") is True
    assert limiter.check("key1") is False
    time.sleep(1.1)
    assert limiter.check("key1") is True


def test_separate_keys_independent():
    limiter = RateLimiter(limit=1, window=60)
    assert limiter.check("a") is True
    assert limiter.check("a") is False
    assert limiter.check("b") is True


def test_info_returns_correct_data():
    limiter = RateLimiter(limit=5, window=60)
    info = limiter.info("key1")
    assert info.limit == 5
    assert info.remaining == 5
    limiter.check("key1")
    limiter.check("key1")
    info = limiter.info("key1")
    assert info.remaining == 3


def test_info_no_requests():
    limiter = RateLimiter(limit=10, window=60)
    info = limiter.info("nonexistent")
    assert info.limit == 10
    assert info.remaining == 10


def test_get_rate_limiter_from_env(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT", "50")
    monkeypatch.setenv("RATE_LIMIT_WINDOW", "30")
    limiter = get_rate_limiter()
    assert limiter._limit == 50
    assert limiter._window == 30


def test_get_rate_limiter_defaults():
    limiter = get_rate_limiter()
    assert limiter._limit == 100
    assert limiter._window == 60


def test_cleanup_removes_expired():
    limiter = RateLimiter(limit=5, window=1)
    limiter.check("key1")
    limiter.check("key1")
    assert len(limiter._requests["key1"]) == 2
    time.sleep(1.1)
    limiter.check("key1")
    assert len(limiter._requests["key1"]) == 1
