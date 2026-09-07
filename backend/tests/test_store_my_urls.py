"""TDD RED: list_by_owner store tests."""

from __future__ import annotations

from src.store import UrlStore


def test_list_by_owner_returns_user_urls() -> None:
    store = UrlStore()
    store.shorten("https://a.com", user_id=1)
    store.shorten("https://b.com", user_id=1)
    result = store.list_by_owner(user_id=1)
    assert len(result) == 2
    assert result[0]["original_url"] == "https://a.com"
    assert result[1]["original_url"] == "https://b.com"


def test_list_by_owner_excludes_other_users() -> None:
    store = UrlStore()
    store.shorten("https://a.com", user_id=1)
    store.shorten("https://b.com", user_id=2)
    result = store.list_by_owner(user_id=1)
    assert len(result) == 1
    assert result[0]["original_url"] == "https://a.com"


def test_list_by_owner_returns_correct_fields() -> None:
    store = UrlStore()
    store.shorten("https://a.com", user_id=1, custom_id="my-link")
    result = store.list_by_owner(user_id=1)
    item = result[0]
    assert item["short_id"] == "my-link"
    assert item["original_url"] == "https://a.com"
    assert item["short_url"] == "http://localhost:8000/my-link"
    assert item["clicks"] == 0
    assert item["expired"] is False
    assert item["expires_at"] is None
    assert "created_at" in item


def test_list_by_owner_includes_clicks() -> None:
    store = UrlStore()
    sid = store.shorten("https://a.com", user_id=1)
    store.record_click(sid)
    store.record_click(sid)
    result = store.list_by_owner(user_id=1)
    assert result[0]["clicks"] == 2


def test_list_by_owner_expired_flag() -> None:
    store = UrlStore()
    store.shorten("https://a.com", user_id=1, expires_in=1)
    # Force expired
    store._expires_at[store.shorten("https://a.com", user_id=1)] = (
        "2020-01-01T00:00:00Z"
    )
    # Use the one that was forced expired
    sids = [k for k, v in store._url_owner.items() if v == 1]
    for sid in sids:
        store._expires_at[sid] = "2020-01-01T00:00:00Z"
    result = store.list_by_owner(user_id=1)
    assert all(r["expired"] for r in result)


def test_list_by_owner_empty() -> None:
    store = UrlStore()
    result = store.list_by_owner(user_id=999)
    assert result == []
