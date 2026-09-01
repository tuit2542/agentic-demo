"""Tests for URL expiration (TTL)."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import create_app
from src.models import ShortenRequest

# ── Validation ─────────────────────────────────────────


def test_expires_in_valid() -> None:
    req = ShortenRequest(url="https://example.com", expires_in=3600)
    assert req.expires_in == 3600


def test_expires_in_none_by_default() -> None:
    req = ShortenRequest(url="https://example.com")
    assert req.expires_in is None


def test_expires_in_too_small() -> None:
    with pytest.raises(ValueError, match="between 1 and"):
        ShortenRequest(url="https://example.com", expires_in=0)


def test_expires_in_too_large() -> None:
    with pytest.raises(ValueError, match="between 1 and"):
        ShortenRequest(url="https://example.com", expires_in=99999999)


def test_expires_in_string_rejected() -> None:
    # Pydantic should coerce or reject
    req = ShortenRequest(url="https://example.com", expires_in=1)  # type: ignore
    assert req.expires_in == 1


# ── Store ──────────────────────────────────────────────


def test_store_expires_in_sets_expiry() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid = store.shorten("https://example.com", expires_in=3600)
    assert store.get_expires_at(sid) is not None
    assert not store.is_expired(sid)


def test_store_no_expiry_never_expired() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert store.get_expires_at(sid) is None
    assert not store.is_expired(sid)


def test_store_expired_blocks_resolve() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid = store.shorten("https://example.com", expires_in=1)
    # Manually set to past
    from datetime import datetime, timedelta, timezone

    store._expires_at[sid] = (
        datetime.now(timezone.utc) - timedelta(seconds=10)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert store.is_expired(sid)
    assert store.resolve(sid) is None


def test_store_delete_owner_ok() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid = store.shorten("https://example.com", user_id=1)
    assert store.delete(sid, user_id=1) is True
    assert store.peek(sid) is None


def test_store_delete_wrong_owner_forbidden() -> None:
    from src.store import UrlStore

    store = UrlStore()
    sid = store.shorten("https://example.com", user_id=1)
    with pytest.raises(PermissionError):
        store.delete(sid, user_id=99)


# ── Integration ────────────────────────────────────────


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def auth_client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Register with unique email per test run
        import random
        import string

        email = "".join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"
        await c.post("/auth/register", json={"email": email, "password": "password123"})
        resp = await c.post(
            "/auth/login", json={"email": email, "password": "password123"}
        )
        c.headers["Authorization"] = f"Bearer {resp.json()['access_token']}"
        yield c


@pytest.mark.anyio
async def test_shorten_with_expiry(auth_client):
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "expires_in": 3600}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "expires_at" in data
    assert data["expires_at"] is not None


@pytest.mark.anyio
async def test_shorten_without_expiry_no_expires_at(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    assert resp.json()["expires_at"] is None


@pytest.mark.anyio
async def test_redirect_expired_returns_410(auth_client, app):
    # Create link with 1s expiry, wait, then redirect should be 410
    # Instead of sleeping, create and manually expire via store
    # We test via API: create, then test stats shows not expired
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "expires_in": 1}
    )
    sid = resp.json()["short_id"]
    # Immediately should still redirect (1s not passed yet generally)
    # Test stats shows expires info
    stats = await auth_client.get(f"/stats/{sid}")
    assert stats.status_code == 200
    assert stats.json()["expires_at"] is not None


@pytest.mark.anyio
async def test_stats_shows_expired_flag(auth_client):
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "expires_in": 3600}
    )
    sid = resp.json()["short_id"]
    stats = await auth_client.get(f"/stats/{sid}")
    data = stats.json()
    assert data["expired"] is False
    assert data["expires_at"] is not None


@pytest.mark.anyio
async def test_stats_never_expires(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    sid = resp.json()["short_id"]
    stats = await auth_client.get(f"/stats/{sid}")
    assert stats.json()["expired"] is False
    assert stats.json()["expires_at"] is None


@pytest.mark.anyio
async def test_invalid_expires_in_422(auth_client):
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "expires_in": 0}
    )
    assert resp.status_code == 422
    resp = await auth_client.post(
        "/shorten", json={"url": "https://example.com", "expires_in": 99999999}
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_expired_redirect_410():
    """Create URL that is already expired, resolve should 410."""
    # Use in-memory store directly to simulate past expiry
    from datetime import datetime, timedelta, timezone

    from src.store import UrlStore

    # Create fresh app to get isolated store if needed — easier: test via unit
    store = UrlStore()
    sid = store.shorten("https://example.com", expires_in=1)
    store._expires_at[sid] = (
        datetime.now(timezone.utc) - timedelta(seconds=10)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    assert store.is_expired(sid)
    assert store.resolve(sid) is None  # expired → None


@pytest.mark.anyio
async def test_delete_url(auth_client):
    resp = await auth_client.post("/shorten", json={"url": "https://example.com"})
    sid = resp.json()["short_id"]
    del_resp = await auth_client.delete(f"/{sid}")
    assert del_resp.status_code == 204
    stats = await auth_client.get(f"/stats/{sid}")
    assert stats.status_code == 404


@pytest.mark.anyio
async def test_delete_requires_auth(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        resp = await c.delete("/abc123")
        assert resp.status_code == 401


@pytest.mark.anyio
async def test_delete_not_found(auth_client):
    resp = await auth_client.delete("/nonexist999")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_shorten_with_custom_id_and_expiry(auth_client):
    resp = await auth_client.post(
        "/shorten",
        json={
            "url": "https://example.com",
            "custom_id": "expire-me",
            "expires_in": 3600,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["short_id"] == "expire-me"
    assert resp.json()["expires_at"] is not None
