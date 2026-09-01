from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import create_app
from src.rate_limiter import RateLimiter


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.anyio
async def test_shorten_returns_201(client):
    resp = await client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    data = resp.json()
    assert "short_id" in data
    assert "short_url" in data


@pytest.mark.anyio
async def test_shorten_returns_rate_limit_headers(client):
    resp = await client.post("/shorten", json={"url": "https://example.com"})
    assert "X-RateLimit-Limit" in resp.headers
    assert "X-RateLimit-Remaining" in resp.headers
    assert "X-RateLimit-Reset" in resp.headers


@pytest.mark.anyio
async def test_redirect_moves_to_original(client):
    resp = await client.post("/shorten", json={"url": "https://example.com"})
    sid = resp.json()["short_id"]
    resp2 = await client.get(f"/{sid}", follow_redirects=False)
    assert resp2.status_code == 307
    assert resp2.headers["location"] == "https://example.com/"


@pytest.mark.anyio
async def test_stats_returns_count(client):
    resp = await client.post("/shorten", json={"url": "https://example.com"})
    sid = resp.json()["short_id"]
    await client.get(f"/{sid}")
    await client.get(f"/{sid}")
    resp = await client.get(f"/stats/{sid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["clicks"] == 2
    assert "clicks_history" in data
    assert len(data["clicks_history"]) == 2
    assert "timestamp" in data["clicks_history"][0]


@pytest.mark.anyio
async def test_shorten_invalid_url_returns_422(client):
    resp = await client.post("/shorten", json={"url": "not-a-url"})
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_redirect_unknown_returns_404(client):
    resp = await client.get("/zzzzzz")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_stats_unknown_returns_404(client):
    resp = await client.get("/stats/zzzzzz")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_rate_limit_shorten_returns_429():
    """Test rate limiting with small limit."""
    # Create app with overridden limiter via monkeypatch on module level
    import src.app as app_module

    original_fn = app_module.get_rate_limiter
    app_module.get_rate_limiter = lambda: RateLimiter(limit=2, window=60)
    try:
        app = create_app()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            resp = await c.post("/shorten", json={"url": "https://example.com"})
            assert resp.status_code == 201
            resp = await c.post("/shorten", json={"url": "https://example2.com"})
            assert resp.status_code == 201
            resp = await c.post("/shorten", json={"url": "https://example3.com"})
            assert resp.status_code == 429
            assert "Rate limit exceeded" in resp.json()["detail"]
            assert "X-RateLimit-Limit" in resp.headers
    finally:
        app_module.get_rate_limiter = original_fn


@pytest.mark.anyio
async def test_rate_limit_stats_no_limit(client):
    # Stats should NOT be rate limited — no limit key, just check 404
    for _ in range(10):
        resp = await client.get("/stats/zzzzzz")
        assert resp.status_code == 404  # 404 not 429
