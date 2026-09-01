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


@pytest.fixture
async def auth_client(app):
    """Client with authenticated user."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Register + login
        await c.post(
            "/auth/register",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        resp = await c.post(
            "/auth/login",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        token = resp.json()["access_token"]
        c.headers["Authorization"] = f"Bearer {token}"
        yield c


@pytest.mark.anyio
async def test_shorten_returns_201(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    data = resp.json()
    assert "short_id" in data
    assert "short_url" in data


@pytest.mark.anyio
async def test_shorten_requires_auth(client):
    resp = await client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_shorten_returns_rate_limit_headers(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    assert "X-RateLimit-Limit" in resp.headers
    assert "X-RateLimit-Remaining" in resp.headers
    assert "X-RateLimit-Reset" in resp.headers


@pytest.mark.anyio
async def test_redirect_moves_to_original(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(f"/{sid}", follow_redirects=False)
    assert resp2.status_code == 307
    assert resp2.headers["location"].rstrip("/") == "https://example.com"


@pytest.mark.anyio
async def test_stats_returns_count(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    sid = resp.json()["short_id"]
    await auth_client.get(f"/{sid}")
    await auth_client.get(f"/{sid}")
    resp = await auth_client.get(f"/stats/{sid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["clicks"] == 2
    assert "clicks_history" in data
    assert len(data["clicks_history"]) == 2
    assert "timestamp" in data["clicks_history"][0]


@pytest.mark.anyio
async def test_shorten_invalid_url_returns_422(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "not-a-url"})
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
    import src.app as app_module
    import src.auth as auth_module

    original_fn = app_module.get_rate_limiter
    app_module.get_rate_limiter = lambda: RateLimiter(limit=2, window=60)
    original_repo = auth_module._user_repo
    auth_module._user_repo = None
    try:
        app = create_app()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            # Register + login
            await c.post(
                "/auth/register",
                json={"email": "rltest@example.com", "password": "password123"},
            )
            resp = await c.post(
                "/auth/login",
                json={"email": "rltest@example.com", "password": "password123"},
            )
            token = resp.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            resp = await c.post(
                "/shorten", json={"url": "https://example.com"}, headers=headers
            )
            assert resp.status_code == 201
            resp = await c.post(
                "/shorten", json={"url": "https://example2.com"}, headers=headers
            )
            assert resp.status_code == 201
            resp = await c.post(
                "/shorten", json={"url": "https://example3.com"}, headers=headers
            )
            assert resp.status_code == 429
            assert "Rate limit exceeded" in resp.json()["detail"]
            assert "X-RateLimit-Limit" in resp.headers
    finally:
        app_module.get_rate_limiter = original_fn
        auth_module._user_repo = original_repo


@pytest.mark.anyio
async def test_rate_limit_stats_no_limit(client):
    # Stats should NOT be rate limited — no limit key, just check 404
    for _ in range(10):
        resp = await client.get("/stats/zzzzzz")
        assert resp.status_code == 404  # 404 not 429


@pytest.mark.anyio
async def test_shorten_anon_works(client):
    resp = await client.post("/shorten-anon", json={"url": "https://example.com"})
    assert resp.status_code == 201
    assert "short_id" in resp.json()
