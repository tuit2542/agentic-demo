"""TDD RED: Password-protected links — model + store + endpoint tests."""

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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post(
            "/auth/register",
            json={"email": "pwprotect@example.com", "password": "password123"},
        )
        resp = await c.post(
            "/auth/login",
            json={"email": "pwprotect@example.com", "password": "password123"},
        )
        token = resp.json()["access_token"]
        c.headers["Authorization"] = f"Bearer {token}"
        yield c


@pytest.mark.anyio
async def test_shorten_with_password_returns_is_protected(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["is_protected"] is True
    assert "short_id" in data


@pytest.mark.anyio
async def test_shorten_without_password_no_protected(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["is_protected"] is False


@pytest.mark.anyio
async def test_protected_link_requires_password(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "secret123"},
    )
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(f"/{sid}", follow_redirects=False)
    assert resp2.status_code == 401
    assert "Password required" in resp2.json()["detail"]


@pytest.mark.anyio
async def test_protected_link_correct_password_redirects(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "secret123"},
    )
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(f"/{sid}?password=secret123", follow_redirects=False)
    assert resp2.status_code == 307
    assert resp2.headers["location"].rstrip("/") == "https://example.com"


@pytest.mark.anyio
async def test_protected_link_wrong_password_401(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "secret123"},
    )
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(f"/{sid}?password=wrong", follow_redirects=False)
    assert resp2.status_code == 401
    assert "Invalid password" in resp2.json()["detail"]


@pytest.mark.anyio
async def test_password_too_short_returns_422(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "ab"},
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_password_too_long_returns_422(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "x" * 65},
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_unprotected_link_works_without_password(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com"},
    )
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(f"/{sid}", follow_redirects=False)
    assert resp2.status_code == 307
    assert resp2.headers["location"].rstrip("/") == "https://example.com"


@pytest.mark.anyio
async def test_protected_link_x_header_password(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "secret123"},
    )
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(
        f"/{sid}",
        headers={"X-Link-Password": "secret123"},
        follow_redirects=False,
    )
    assert resp2.status_code == 307


@pytest.mark.anyio
async def test_protected_link_stats_still_public(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={"url": "https://example.com", "password": "secret123"},
    )
    sid = resp.json()["short_id"]
    resp2 = await auth_client.get(f"/stats/{sid}")
    assert resp2.status_code == 200
    assert resp2.json()["clicks"] == 0
