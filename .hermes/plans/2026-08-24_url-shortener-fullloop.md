# URL Shortener — Agentic Full-Loop Demo

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a minimal URL shortener API demonstrating the full agentic dev loop.

**Architecture:** Flask in-memory store, TDD at every step, pre-commit verification, auto-PR.

**Tech Stack:** Python 3.11, Flask, pytest, ruff

---

## Task 1: Project scaffolding

**Objective:** Create package structure, empty __init__.py, conftest.py

**Files:**
- Create: `src/__init__.py`
- Create: `src/store.py` (empty stub)
- Create: `src/app.py` (empty stub)
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

**Step 1:** Create directories and empty files.

**Step 2:** Verify with `ruff check src/ tests/` — no errors.

---

## Task 2: In-memory URL store (TDD)

**Objective:** Store that maps short_id → original_url, tracks click count.

**Files:**
- Create: `tests/test_store.py`
- Create: `src/store.py`

### Step 1: Write failing test

```python
from src.store import UrlStore

def test_shorten_returns_short_id():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert isinstance(sid, str)
    assert len(sid) == 6

def test_resolve_returns_original_url():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    assert store.resolve(sid) == "https://example.com"

def test_resolve_unknown_returns_none():
    store = UrlStore()
    assert store.resolve("zzzzzz") is None

def test_click_count_increments():
    store = UrlStore()
    sid = store.shorten("https://example.com")
    store.resolve(sid)
    store.resolve(sid)
    assert store.stats(sid) == 2

def test_stats_unknown_returns_zero():
    store = UrlStore()
    assert store.stats("zzzzzz") == 0
```

### Step 2: Run to verify RED

`pytest tests/test_store.py -v` → FAIL

### Step 3: Minimal implementation

```python
import string
import random

class UrlStore:
    def __init__(self):
        self._urls = {}
        self._clicks = {}

    def shorten(self, url: str) -> str:
        sid = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        while sid in self._urls:
            sid = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self._urls[sid] = url
        self._clicks[sid] = 0
        return sid

    def resolve(self, sid: str) -> str | None:
        if sid in self._urls:
            self._clicks[sid] += 1
            return self._urls[sid]
        return None

    def stats(self, sid: str) -> int:
        return self._clicks.get(sid, 0)
```

### Step 4: Run to verify GREEN

`pytest tests/test_store.py -v` → PASS

### Step 5: Commit

```bash
git add src/store.py tests/test_store.py
git commit -m "feat: add UrlStore with shorten/resolve/stats"
```

---

## Task 3: Flask API (TDD)

**Objective:** REST endpoints for shorten, redirect, stats.

**Files:**
- Create: `tests/test_app.py`
- Create: `src/app.py`

### Step 1: Write failing tests

```python
from src.app import create_app

def test_shorten_returns_201():
    app = create_app()
    resp = app.test_client().post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 201
    assert "short_id" in resp.json

def test_redirect_moves_to_original():
    app = create_app()
    resp = app.test_client().post("/shorten", json={"url": "https://example.com"})
    sid = resp.json["short_id"]
    resp2 = app.test_client().get(f"/{sid}", follow_redirects=False)
    assert resp2.status_code == 302
    assert resp2.headers["Location"] == "https://example.com"

def test_stats_returns_count():
    app = create_app()
    client = app.test_client()
    sid = client.post("/shorten", json={"url": "https://example.com"}).json["short_id"]
    client.get(f"/{sid}")
    client.get(f"/{sid}")
    resp = client.get(f"/stats/{sid}")
    assert resp.status_code == 200
    assert resp.json["clicks"] == 2

def test_shorten_missing_url_returns_400():
    app = create_app()
    resp = app.test_client().post("/shorten", json={})
    assert resp.status_code == 400

def test_redirect_unknown_returns_404():
    app = create_app()
    resp = app.test_client().get("/zzzzzz")
    assert resp.status_code == 404
```

### Step 2: Run to verify RED

`pytest tests/test_app.py -v` → FAIL

### Step 3: Minimal implementation

```python
from flask import Flask, request, jsonify, redirect
from src.store import UrlStore

def create_app():
    app = Flask(__name__)
    store = UrlStore()

    @app.post("/shorten")
    def shorten():
        data = request.get_json(silent=True) or {}
        url = data.get("url")
        if not url:
            return jsonify({"error": "url is required"}), 400
        sid = store.shorten(url)
        return jsonify({"short_id": sid}), 201

    @app.get("/<sid>")
    def redirect_url(sid):
        url = store.resolve(sid)
        if url is None:
            return jsonify({"error": "not found"}), 404
        return redirect(url)

    @app.get("/stats/<sid>")
    def stats(sid):
        clicks = store.stats(sid)
        return jsonify({"short_id": sid, "clicks": clicks})

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
```

### Step 4: Run to verify GREEN

`pytest tests/ -v` → ALL PASS

### Step 5: Commit

```bash
git add src/app.py tests/test_app.py
git commit -m "feat: add Flask API endpoints"
```

---

## Task 4: Lint + Pre-commit verification

**Objective:** Run ruff, security scan, full test suite.

**Step 1:** `ruff check src/ tests/` → 0 errors

**Step 2:** Run full test suite → all green

**Step 3:** Commit if anything was fixed.

---

## Task 5: Final commit + tag

**Objective:** Tag v0.1.0

```bash
git tag v0.1.0
```
