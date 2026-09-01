"""Tests for JWT auth — TDD RED phase."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import create_app
from src.auth import create_token, hash_password, verify_password, verify_token

# ── Unit tests ─────────────────────────────────────────


def test_hash_and_verify_password() -> None:
    hashed = hash_password("mysecret123")
    assert verify_password("mysecret123", hashed) is True
    assert verify_password("wrongpass", hashed) is False


def test_create_and_verify_token() -> None:
    token = create_token(1, "test@example.com")
    payload = verify_token(token)
    assert payload["sub"] == "1"
    assert payload["email"] == "test@example.com"


def test_verify_invalid_token_raises() -> None:
    from fastapi import HTTPException as _E

    with pytest.raises(_E):
        verify_token("invalid.jwt.token")


# ── Integration tests ──────────────────────────────────


@pytest.mark.asyncio
async def test_register_success() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/auth/register",
            json={"email": "alice@example.com", "password": "password123"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "alice@example.com"
        assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={"email": "bob@example.com", "password": "password123"},
        )
        resp = await client.post(
            "/auth/register",
            json={"email": "bob@example.com", "password": "password123"},
        )
        assert resp.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_email() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/auth/register", json={"email": "not-an-email", "password": "password123"}
        )
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/auth/register", json={"email": "x@example.com", "password": "short"}
        )
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_success() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={"email": "carol@example.com", "password": "password123"},
        )
        resp = await client.post(
            "/auth/login",
            json={"email": "carol@example.com", "password": "password123"},
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={"email": "dave@example.com", "password": "password123"},
        )
        resp = await client.post(
            "/auth/login", json={"email": "dave@example.com", "password": "wrongpass1"}
        )
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_auth_me() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={"email": "eve@example.com", "password": "password123"},
        )
        login = await client.post(
            "/auth/login", json={"email": "eve@example.com", "password": "password123"}
        )
        token = login.json()["access_token"]
        resp = await client.get(
            "/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200
        assert resp.json()["email"] == "eve@example.com"


@pytest.mark.asyncio
async def test_shorten_requires_auth() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/shorten", json={"url": "https://example.com"})
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_shorten_with_auth() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={"email": "frank@example.com", "password": "password123"},
        )
        login = await client.post(
            "/auth/login",
            json={"email": "frank@example.com", "password": "password123"},
        )
        token = login.json()["access_token"]
        resp = await client.post(
            "/shorten",
            json={"url": "https://example.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        assert "short_id" in resp.json()


@pytest.mark.asyncio
async def test_shorten_anon_still_works() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/shorten-anon", json={"url": "https://example.com"})
        assert resp.status_code == 201
