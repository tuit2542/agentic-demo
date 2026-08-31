# API Reference

> Agentic Demo — URL Shortener

---

## Endpoints

| Endpoint | Method | Request Body | Response | Description |
|----------|--------|--------------|----------|-------------|
| `/health` | GET | - | `{"status": "ok"}` | Health check |
| `/shorten` | POST | `{"url": "https://example.com"}` | `{"short_id": "abc123", "short_url": "http://localhost/abc123"}` | สร้าง short URL |
| `/stats/{sid}` | GET | - | `{"short_id": "abc123", "clicks": 5, "original_url": "..."}` | ดูสถิติ |
| `/{sid}` | GET | - | 307 Redirect → original URL | Redirect |

---

## Models

| Model | Fields | Description |
|-------|--------|-------------|
| `ShortenRequest` | `url: str` (validated) | Validate input ตอนสร้าง short URL |
| `ShortenResponse` | `short_id: str`, `short_url: str` | Response ตอนสร้าง short URL |
| `StatsResponse` | `short_id: str`, `clicks: int`, `original_url: str` | Response ตอนดูสถิติ |

---

## Store

| Class | Methods | Description |
|-------|---------|-------------|
| `UrlStore` | `shorten(url) -> short_id` | สร้าง short ID จาก URL |
| `UrlStore` | `resolve(short_id) -> url` | หา original URL จาก short ID |
| `UrlStore` | `stats(short_id) -> int` | ดู click count |

**Logic:**
- Short ID: 6-char alphanumeric (a-z, A-Z, 0-9)
- Storage: Python dict (in-memory, ไม่ persist)
- Click count: เพิ่มทุกครั้งที่ resolve

---

## Examples

**สร้าง short URL:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very-long-url"}'
```

Response:
```json
{
  "short_id": "AbC123",
  "short_url": "http://localhost/AbC123"
}
```

**ดูสถิติ:**
```bash
curl http://localhost:8000/stats/AbC123
```

Response:
```json
{
  "short_id": "AbC123",
  "clicks": 5,
  "original_url": "https://example.com/very-long-url"
}
```

---

## Tests

| File | Tests | Status |
|------|-------|--------|
| `tests/test_store.py` | 5 tests | ✅ |
| `tests/test_models.py` | 5 tests | ✅ |
| `tests/test_app.py` | 6 tests | ✅ |
| **Total** | **16 tests** | **✅ All pass** |

---

*Last updated: 2026-08-31*
