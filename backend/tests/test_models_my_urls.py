"""TDD RED: My Links Dashboard — backend failing tests."""
from __future__ import annotations

from src.models import UserUrlItem, UserUrlsResponse


def test_user_url_item_fields() -> None:
    item = UserUrlItem(
        short_id="abc",
        original_url="https://example.com",
        short_url="http://localhost:8000/abc",
        clicks=5,
        expired=False,
        expires_at=None,
        created_at="2026-09-07T10:00:00Z",
    )
    assert item.short_id == "abc"
    assert item.clicks == 5
    assert item.expired is False


def test_user_url_item_with_expiry() -> None:
    item = UserUrlItem(
        short_id="xyz",
        original_url="https://example.com",
        short_url="http://localhost:8000/xyz",
        clicks=0,
        expired=True,
        expires_at="2026-09-06T10:00:00Z",
        created_at="2026-09-01T10:00:00Z",
    )
    assert item.expired is True
    assert item.expires_at is not None


def test_user_urls_response() -> None:
    item = UserUrlItem(
        short_id="a",
        original_url="https://a.com",
        short_url="http://localhost:8000/a",
        clicks=1,
        expired=False,
        expires_at=None,
        created_at="2026-09-07T10:00:00Z",
    )
    resp = UserUrlsResponse(urls=[item], total=1)
    assert len(resp.urls) == 1
    assert resp.total == 1
