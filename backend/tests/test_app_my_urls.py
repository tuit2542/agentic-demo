"""TDD RED: GET /my/urls endpoint tests."""
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


@pytest.fixture
async def auth_client(app):
    """Client with authenticated user."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post(
            "/auth/register",
            json={"email": "mylinks@example.com", "password": "password123"},
        )
        resp = await c.post(
            "/auth/login",
            json={"email": "mylinks@example.com", "password": "password123"},
        )
        token = resp.json()["access_token"]
        c.headers["Authorization"] = f"Bearer {token}"
        yield c


@pytest.mark.anyio
async def test_my_urls_requires_auth(client):
    resp = await client.get("/my/urls")
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_my_urls_returns_empty_list(auth_client):
    resp = await auth_client.get("/my/urls")
    assert resp.status_code == 200
    data = resp.json()
    assert data["urls"] == []
    assert data["total"] == 0


@pytest.mark.anyio
async def test_my_urls_returns_created_urls(auth_client):
    await auth_client.post("/shorten", json={"url": "https://example.com"})
    await auth_client.post("/shorten", json={"url": "https://test.com"})
    resp = await auth_client.get("/my/urls")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["urls"]) == 2


@pytest.mark.anyio
async def test_my_urls_has_correct_fields(auth_client):
    await auth_client.post("/shorten", json={"url": "https://example.com"})
    resp = await auth_client.get("/my/urls")
    item = resp.json()["urls"][0]
    assert "short_id" in item
    assert "original_url" in item
    assert "short_url" in item
    assert "clicks" in item
    assert "expired" in item
    assert "created_at" in item


@pytest.mark.anyio
async def test_my_urls_only_own_urls(auth_client, client):
    """User should only see their own URLs, not other users'."""
    await auth_client.post("/shorten", json={"url": "https://mine.com"})

    # Another user creates a URL
    await client.post(
        "/auth/register",
        json={"email": "other@example.com", "password": "password123"},
    )
    login_resp = await client.post(
        "/auth/login",
        json={"email": "other@example.com", "password": "password123"},
    )
    other_token = login_resp.json()["access_token"]
    await client.post(
        "/shorten",
        json={"url": "https://theirs.com"},
        headers={"Authorization": f"Bearer {other_token}"},
    )

    resp = await auth_client.get("/my/urls")
    assert resp.json()["total"] == 1
    assert resp.json()["urls"][0]["original_url"] == "https://mine.com"
