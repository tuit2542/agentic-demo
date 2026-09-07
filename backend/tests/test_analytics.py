"""Analytics dashboard — RED tests (TDD step 1: failing)."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestAnalyticsModels:
    """Pydantic model validation."""

    def test_referrer_stat_fields(self) -> None:
        from src.models import ReferrerStat

        stat = ReferrerStat(referrer="https://twitter.com", count=10)
        assert stat.referrer == "https://twitter.com"
        assert stat.count == 10

    def test_referrer_stat_null(self) -> None:
        from src.models import ReferrerStat

        stat = ReferrerStat(referrer=None, count=5)
        assert stat.referrer is None
        assert stat.count == 5

    def test_analytics_response_fields(self) -> None:
        from src.models import AnalyticsResponse

        resp = AnalyticsResponse(
            short_id="abc",
            total_clicks=10,
            unique_referrers=3,
            top_referrers=[],
            clicks_by_hour={},
            recent_clicks=[],
            expired=False,
            expires_at=None,
        )
        assert resp.short_id == "abc"
        assert resp.total_clicks == 10


class TestStoreAnalytics:
    def test_no_clicks(self) -> None:
        from src.store import UrlStore

        store = UrlStore()
        sid = store.shorten("https://example.com")
        result = store.get_analytics(sid)
        assert result["total_clicks"] == 0
        assert result["unique_referrers"] == 0
        assert result["top_referrers"] == []  # type: ignore

    def test_with_clicks(self) -> None:
        from src.store import UrlStore

        store = UrlStore()
        sid = store.shorten("https://example.com")
        store.record_click(sid, referrer="https://twitter.com")
        store.record_click(sid, referrer="https://twitter.com")
        store.record_click(sid, referrer="https://facebook.com")
        store.record_click(sid, referrer=None)
        result = store.get_analytics(sid)
        assert result["total_clicks"] == 4
        assert result["unique_referrers"] == 2

    def test_nonexistent(self) -> None:
        from src.store import UrlStore

        store = UrlStore()
        result = store.get_analytics("nonexistent")
        assert result["total_clicks"] == 0


@pytest.mark.anyio
async def test_analytics_success(client):
    """AC-1: valid short_id → analytics."""
    res = await client.post("/shorten-anon", json={"url": "https://example.com"})
    sid = res.json()["short_id"]
    res = await client.get(f"/analytics/{sid}")
    assert res.status_code == 200
    assert res.json()["short_id"] == sid


@pytest.mark.anyio
async def test_analytics_not_found(client):
    """AC-3: non-existent → 404."""
    res = await client.get("/analytics/doesnotexist")
    assert res.status_code == 404
