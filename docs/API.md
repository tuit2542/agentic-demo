# API Reference

> Agentic Demo — URL Shortener

---

## Endpoints

| Endpoint | Method | Request Body | Response | ใช้ทำอะไร |
|----------|--------|--------------|----------|----------|
| `/` | GET | - | `{"message": "URL Shortener API"}` | Health check |
| `/shorten` | POST | `{"url": "https://example.com"}` | `{"short_id": "abc123", "original_url": "..."}` | สร้าง short URL |
| `/{short_id}` | GET | - | 307 Redirect | Redirect ไป original URL |
| `/{short_id}/stats` | GET | - | `{"short_id": "abc123", "original_url": "...", "clicks": 5}` | ดูสถิติ |

---

## Models

| Model | Fields | ใช้ทำอะไร |
|-------|--------|----------|
| `ShortenRequest` | `url: str` (validated) | Validate input ตอนสร้าง short URL |
| `ShortenResponse` | `short_id: str`, `original_url: str`, `created_at: str` | Response ตอนสร้าง short URL |
| `StatsResponse` | `short_id: str`, `original_url: str`, `clicks: int` | Response ตอนดูสถิติ |

---

## Store

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
| `tests/test_store.py` | 5 tests | ✅ |
| `tests/test_models.py` | 5 tests | ✅ |
| `tests/test_app.py` | 6 tests | ✅ |
| **Total** | **16 tests** | **✅ All pass** |

---

*Last updated: 2026-08-27*