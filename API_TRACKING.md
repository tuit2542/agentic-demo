# API Tracking

> บันทึกว่า src code ทำอะไร มี API อะไรบ้าง ใช้ทำอะไร

---

## Project Overview

**ชื่อ:** Agentic Demo — URL Shortener
**Stack:** Python 3.11, FastAPI, Pydantic v2, pytest, ruff, mypy
**สถานะ:** v0.2.0 — MVP พร้อมใช้งาน

---

## Source Files

### `src/app.py` — FastAPI Application

| API Endpoint | Method | Request Body | Response | ใช้ทำอะไร |
|-------------|--------|--------------|----------|----------|
| `/` | GET | - | `{"message": "URL Shortener API"}` | Health check |
| `/shorten` | POST | `{"url": "https://example.com"}` | `{"short_id": "abc123", "original_url": "..."}` | สร้าง short URL |
| `/{short_id}` | GET | - | 307 Redirect | Redirect ไป original URL |
| `/{short_id}/stats` | GET | - | `{"short_id": "abc123", "original_url": "...", "clicks": 5}` | ดูสถิติ |

### `src/models.py` — Pydantic Models

| Model | Fields | ใช้ทำอะไร |
|-------|--------|----------|
| `ShortenRequest` | `url: str` (validated) | Validate input ตอนสร้าง short URL |
| `ShortenResponse` | `short_id: str`, `original_url: str`, `created_at: str` | Response ตอนสร้าง short URL |
| `StatsResponse` | `short_id: str`, `original_url: str`, `clicks: int` | Response ตอนดูสถิติ |

### `src/store.py` — In-Memory Storage

| Class | Methods | ใช้ทำอะไร |
|-------|---------|----------|
| `UrlStore` | `shorten(url) -> short_id` | สร้าง short ID จาก URL |
| `UrlStore` | `resolve(short_id) -> url` | หา original URL จาก short ID |
| `UrlStore` | `stats(short_id) -> dict` | ดูข้อมูล + click count |

**Logic:**
- Short ID: 6-char alphanumeric (a-z, A-Z, 0-9)
- Storage: Python dict (in-memory, ไม่ persist)
- Click count: เพิ่มทุกครั้งที่ resolve

---

## Tests

| File | Tests | Status |
|------|-------|--------|
| `tests/test_store.py` | 5 tests (shorten, resolve, not found, duplicate, missing) | ✅ |
| `tests/test_models.py` | 5 tests (valid, empty, missing, response fields) | ✅ |
| `tests/test_app.py` | 6 tests (201, redirect, stats, 422, 404) | ✅ |
| **Total** | **16 tests** | **✅ All pass** |

---

## Validation Pipeline

| Check | Command | Must Pass |
|-------|---------|-----------|
| Lint | `python -m ruff check src/ tests/` | ✅ |
| Type check | `python -m mypy src/ --ignore-missing-imports` | ✅ |
| Tests | `python -m pytest tests/ -v` | ✅ |
| Security | `python -m pip-audit --desc` | ⚠️ warn-only |

---

## Future Features (ถ้าจะเพิ่ม)

| Feature | Priority | สถานะ |
|---------|----------|--------|
| SQLite/PostgreSQL storage | 🔴 สูง | ❌ ยังไม่มี |
| Rate limiting | 🔴 สูง | ❌ ยังไม่มี |
| JWT authentication | 🟡 กลาง | ❌ ยังไม่มี |
| Custom short ID | 🟡 กลาง | ❌ ยังไม่มี |
| URL expiration | 🟡 กลาง | ❌ ยังไม่มี |
| Click analytics | 🟢 ต่ำ | ❌ ยังไม่มี |

---

*Last updated: 2026-08-27*
