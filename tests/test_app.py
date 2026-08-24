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


@pytest.mark.anyio
async def test_shorten_returns_201(client):
    resp = await client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    data = resp.json()
    assert "short_id" in data
    assert "short_url" in data


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
