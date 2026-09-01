"""Tests for custom short ID — TDD RED phase."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import create_app
from src.models import ShortenRequest

# ── Unit tests: ShortenRequest validation ──────────────


def test_shorten_request_with_valid_custom_id() -> None:
    req = ShortenRequest(url="https://example.com", custom_id="my-link")
    assert req.custom_id == "my-link"


def test_shorten_request_custom_id_none_by_default() -> None:
    req = ShortenRequest(url="https://example.com")
    assert req.custom_id is None


def test_custom_id_too_short() -> None:
    with pytest.raises(ValueError, match="3-20 characters"):
        ShortenRequest(url="https://example.com", custom_id="ab")


def test_custom_id_too_long() -> None:
    with pytest.raises(ValueError, match="3-20 characters"):
        ShortenRequest(url="https://example.com", custom_id="a" * 21)


def test_custom_id_invalid_chars() -> None:
    with pytest.raises(ValueError, match="letters, numbers"):
        ShortenRequest(url="https://example.com", custom_id="my link!")


def test_custom_id_with_hyphens_underscores() -> None:
    req = ShortenRequest(url="https://example.com", custom_id="my-link_v2")
    assert req.custom_id == "my-link_v2"


def test_custom_id_reserved_health() -> None:
    with pytest.raises(ValueError, match="reserved"):
        ShortenRequest(url="https://example.com", custom_id="health")


def test_custom_id_reserved_stats() -> None:
    with pytest.raises(ValueError, match="reserved"):
        ShortenRequest(url="https://example.com", custom_id="stats")


def test_custom_id_reserved_auth() -> None:
    with pytest.raises(ValueError, match="reserved"):
        ShortenRequest(url="https://example.com", custom_id="auth")


def test_custom_id_reserved_shorten() -> None:
    with pytest.raises(ValueError, match="reserved"):
        ShortenRequest(url="https://example.com", custom_id="shorten")


def test_custom_id_empty_string_becomes_none() -> None:
    req = ShortenRequest(url="https://example.com", custom_id="   ")
    assert req.custom_id is None


# ── Store tests ────────────────────────────────────────


def test_store_shorten_custom_id() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid = store.shorten("https://example.com", custom_id="my-brand")
    assert sid == "my-brand"


def test_store_shorten_custom_id_duplicate() -> None:
    from src.store import UrlStore

    store = UrlStore()
    store.shorten("https://example.com", custom_id="my-brand")
    with pytest.raises(ValueError, match="already taken"):
        store.shorten("https://other.com", custom_id="my-brand")


def test_store_shorten_auto_generates_without_custom_id() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid1 = store.shorten("https://example.com")
    sid2 = store.shorten("https://example.com")
    assert sid1 != sid2
    assert len(sid1) == 6


# ── Integration tests ──────────────────────────────────


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def auth_client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post(
            "/auth/register",
            json={"email": "customid@example.com", "password": "password123"},
        )
        resp = await c.post(
            "/auth/login",
            json={"email": "customid@example.com", "password": "password123"},
        )
        c.headers["Authorization"] = f"Bearer {resp.json()['access_token']}"
        yield c


@pytest.mark.anyio
async def test_shorten_with_custom_id(auth_client):
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "custom_id": "my-link"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["short_id"] == "my-link"
    assert "my-link" in data["short_url"]


@pytest.mark.anyio
async def test_shorten_custom_id_redirect_works(auth_client):
    await auth_client.post(
        "/shorten", json={"url": "https://example.com", "custom_id": "go-here"}
    )
    resp = await auth_client.get("/go-here", follow_redirects=False)
    assert resp.status_code == 307
    assert "example.com" in resp.headers["location"]


@pytest.mark.anyio
async def test_shorten_custom_id_stats_works(auth_client):
    await auth_client.post(
        "/shorten", json={"url": "https://example.com", "custom_id": "track-me"}
    )
    await auth_client.get("/track-me")
    resp = await auth_client.get("/stats/track-me")
    assert resp.status_code == 200
    assert resp.json()["clicks"] == 1


@pytest.mark.anyio
async def test_shorten_custom_id_duplicate_409(auth_client):
    await auth_client.post(
        "/shorten", json={"url": "https://example.com", "custom_id": "taken"}
    )
    resp = await auth_client.post(
        "/shorten", json={"url": "https://other.com", "custom_id": "taken"}
    )
    assert resp.status_code == 409
    assert "already taken" in resp.json()["detail"]


@pytest.mark.anyio
async def test_shorten_custom_id_invalid_422(auth_client):
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "custom_id": "x"}
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_shorten_custom_id_reserved_422(auth_client):
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "custom_id": "health"}
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_shorten_without_custom_id_still_works(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    assert len(resp.json()["short_id"]) == 6


@pytest.mark.anyio
async def test_shorten_anon_with_custom_id(auth_client):
    """Even anon endpoint should support custom_id."""
    resp = await auth_client.post(
        "/shorten-anon", json={"url": "https://example.com", "custom_id": "anon-custom"}
    )
    assert resp.status_code == 201
    assert resp.json()["short_id"] == "anon-custom"
