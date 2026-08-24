# URL Shortener — FastAPI Migration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Migrate from Flask to FastAPI with full type safety and auto-validation.

**Architecture:** FastAPI + Pydantic models, async endpoints, mypy strict.

**Tech Stack:** Python 3.11, FastAPI, uvicorn, pytest, ruff, mypy

---

## Task 1: Update project config

**Objective:** Switch deps, update context files, add mypy config

**Files:**
- Modify: `requirements.txt`
- Modify: `.hermes.md`
- Create: `mypy.ini`

---

## Task 2: Pydantic models (TDD)

**Objective:** Type-safe request/response models with validation

**Files:**
- Create: `tests/test_models.py`
- Create: `src/models.py`

### Step 1: Write failing tests

```python
from src.models import ShortenRequest, ShortenResponse, StatsResponse

def test_shorten_request_validates_url():
    req = ShortenRequest(url="https://example.com")
    assert req.url == "https://example.com"

def test_shorten_request_rejects_empty_url():
    from pydantic import ValidationError
    try:
        ShortenRequest(url="")
        assert False, "Should have raised"
    except ValidationError:
        pass

def test_shorten_request_rejects_no_url():
    from pydantic import ValidationError
    try:
        ShortenRequest()
        assert False, "Should have raised"
    except ValidationError:
        pass

def test_shorten_response_fields():
    resp = ShortenResponse(short_id="abc123", short_url="http://localhost/abc123")
    assert resp.short_id == "abc123"

def test_stats_response_fields():
    resp = StatsResponse(short_id="abc123", clicks=5, original_url="https://example.com")
    assert resp.clicks == 5
```

### Step 2: Run to verify RED

`pytest tests/test_models.py -v` → FAIL

### Step 3: Minimal implementation

```python
from pydantic import BaseModel, HttpUrl, Field

class ShortenRequest(BaseModel):
    url: HttpUrl

class ShortenResponse(BaseModel):
    short_id: str
    short_url: str

class StatsResponse(BaseModel):
    short_id: str
    clicks: int
    original_url: str

class ErrorResponse(BaseModel):
    detail: str
```

### Step 4: Run to verify GREEN

### Step 5: Commit

---

## Task 3: FastAPI app (TDD)

**Objective:** Replace Flask app with FastAPI, async endpoints

**Files:**
- Modify: `tests/test_app.py`
- Modify: `src/app.py`

### Step 1: Write failing tests

```python
import pytest
from httpx import AsyncClient, ASGITransport
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
    assert resp2.headers["location"] == "https://example.com"

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
```

### Step 2: Run to verify RED

### Step 3: Minimal implementation

```python
from fastapi import FastAPI, HTTPException, RedirectResponse
from src.store import UrlStore
from src.models import ShortenRequest, ShortenResponse, StatsResponse

def create_app() -> FastAPI:
    app = FastAPI(title="URL Shortener")
    store = UrlStore()

    @app.post("/shorten", response_model=ShortenResponse, status_code=201)
    async def shorten(req: ShortenRequest):
        sid = store.shorten(str(req.url))
        return ShortenResponse(
            short_id=sid,
            short_url=f"http://localhost/{sid}"
        )

    @app.get("/{sid}", response_class=RedirectResponse, status_code=307)
    async def redirect_url(sid: str):
        url = store.resolve(sid)
        if url is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        return RedirectResponse(url=url)

    @app.get("/stats/{sid}", response_model=StatsResponse)
    async def stats(sid: str):
        url = store.resolve.__wrapped__(sid) if hasattr(store.resolve, '__wrapped__') else None
        # Need to get original URL without incrementing clicks
        original = store._urls.get(sid)
        if original is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        clicks = store.stats(sid)
        return StatsResponse(
            short_id=sid,
            clicks=clicks,
            original_url=original
        )

    return app
```

### Step 4: Run to verify GREEN

### Step 5: Commit

---

## Task 4: Type check + full validation pipeline

**Objective:** mypy passes, ruff passes, all tests pass

**Commands:**
```bash
mypy src/ --ignore-missing-imports
ruff check src/ tests/
pytest tests/ -v
```

All three must pass before commit.

---

## Task 5: Final tag

**Objective:** Tag v0.2.0
