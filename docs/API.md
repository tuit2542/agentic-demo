# API Reference

> Agentic Demo — URL Shortener

---

## Endpoints

| Endpoint | Method | Auth | Request Body | Response | Description |
|----------|--------|------|--------------|----------|-------------|
| `/health` | GET | - | - | `{"status": "ok"}` | Health check |
| `/auth/register` | POST | - | `{"email": "user@example.com", "password": "password123"}` | `{"id": 1, "email": "user@example.com", "created_at": "2026-09-01T10:00:00Z"}` | Register user |
| `/auth/login` | POST | - | `{"email": "user@example.com", "password": "password123"}` | `{"access_token": "eyJ...", "token_type": "bearer"}` | Login → JWT |
| `/auth/me` | GET | Bearer | - | `{"id": 1, "email": "user@example.com", "created_at": "..."}` | Current user |
| `/shorten` | POST | Bearer | `{"url": "https://example.com", "custom_id": "my-link", "expires_in": 3600}` | `{"short_id": "my-link", "short_url": "http://localhost:8000/my-link", "expires_at": "2026-09-01T11:00:00Z"}` | สร้าง short URL (auth required) |
| `/shorten-anon` | POST | - | `{"url": "https://example.com", "custom_id": "my-link", "expires_in": 3600}` | same as /shorten | สร้าง short URL (anonymous) |
| `/stats/{sid}` | GET | - | - | `{"short_id": "my-link", "clicks": 5, "original_url": "https://example.com", "clicks_history": [...], "expired": false, "expires_at": null}` | ดูสถิติ |
| `/{sid}` | GET | - | - | 307 Redirect → original URL | Redirect (410 if expired, 429 if rate limited) |
| `/{sid}` | DELETE | Bearer | - | 204 No Content | Delete URL (owner only) |

---

## Models

| Model | Fields | Description |
|-------|--------|-------------|
| `RegisterRequest` | `email: str` (email format), `password: str` (≥8 chars) | Register input |
| `LoginRequest` | `email: str`, `password: str` | Login input |
| `UserResponse` | `id: int`, `email: str`, `created_at: str` | User info |
| `TokenResponse` | `access_token: str`, `token_type: str = "bearer"` | JWT response |
| `ShortenRequest` | `url: str` (http/https), `custom_id: str \| None` (3-20 chars, `[a-zA-Z0-9_-]+`), `expires_in: int \| None` (1–31536000) | Validate input ตอนสร้าง short URL |
| `ShortenResponse` | `short_id: str`, `short_url: str`, `expires_at: str \| None` | Response ตอนสร้าง short URL |
| `ClickRecord` | `timestamp: str`, `referrer: str \| None` | บันทึกรายละเอียดการคลิก |
| `StatsResponse` | `short_id: str`, `clicks: int`, `original_url: str`, `clicks_history: list[ClickRecord]`, `expired: bool`, `expires_at: str \| None` | Response ตอนดูสถิติ |
| `ErrorResponse` | `detail: str` | Error body |

---

## Store

| Class | Methods | Description |
|-------|---------|-------------|
| `UrlStore` | `shorten(url, user_id?, custom_id?, expires_in?) -> short_id` | สร้าง short ID |
| `UrlStore` | `resolve(short_id) -> url \| None` | หา original URL (None ถ้าหมดอายุ) |
| `UrlStore` | `stats(short_id) -> int` | ดู click count |
| `UrlStore` | `record_click(short_id, referrer?) -> ClickRecord` | บันทึก click history |
| `UrlStore` | `get_history(short_id) -> list[ClickRecord]` | ดึง click history |
| `UrlStore` | `peek(short_id) -> url \| None` | ดู URL (ไม่นับ click) |
| `UrlStore` | `is_expired(short_id) -> bool` | เช็คว่าหมดอายุไหม |
| `UrlStore` | `get_expires_at(short_id) -> str \| None` | ดูวันหมดอายุ |
| `UrlStore` | `delete(short_id, user_id) -> bool` | ลบ URL (ต้องเป็น owner) |
| `UrlStore` | `get_owner(short_id) -> int \| None` | ดู owner user_id |
| `UserRepository` | `create_user(email, password_hash) -> User` | สร้าง user |
| `UserRepository` | `get_by_email(email) -> User \| None` | หา user ด้วย email |
| `UserRepository` | `get_by_id(user_id) -> User \| None` | หา user ด้วย id |
| `RateLimiter` | `check(key) -> bool` | เช็ค rate limit (sliding window) |
| `RateLimiter` | `info(key) -> RateLimitInfo` | ดู remaining/reset |

**Logic:**
- Short ID: 6-char alphanumeric (a-z, A-Z, 0-9) หรือ custom [a-zA-Z0-9_-]{3,20}
- Custom ID: ต้องไม่ซ้ำ (409), ไม่ใช่ reserved path (health, stats, docs, redoc, auth, shorten, shorten-anon)
- Expires: `expires_in` (seconds) → `expires_at` (ISO8601 UTC), null = ไม่หมดอายุ
- Storage: In-memory (default) หรือ SQLite (WAL, DATABASE_URL set)
- Click count: เพิ่มทุกครั้งที่ resolve

---

## Examples

**Register + Login:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
# → {"access_token": "eyJ...", "token_type": "bearer"}
```

**สร้าง short URL (with auth):**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very-long-url", "custom_id": "my-link", "expires_in": 3600}'
```

**Response:**
```json
{
  "short_id": "my-link",
  "short_url": "http://localhost:8000/my-link",
  "expires_at": "2026-09-01T11:00:00Z"
}
```

**ดูสถิติ:**
```bash
curl http://localhost:8000/stats/my-link
```

**Response:**
```json
{
  "short_id": "my-link",
  "clicks": 5,
  "original_url": "https://example.com/very-long-url",
  "clicks_history": [
    { "timestamp": "2026-09-01T10:00:00Z", "referrer": null }
  ],
  "expired": false,
  "expires_at": "2026-09-01T11:00:00Z"
}
```

**Redirect (และ expired handling):**
```bash
curl -I http://localhost:8000/my-link
# 307 → Location: https://example.com/very-long-url (ถ้าไม่หมดอายุ)
# 410 {"detail": "Short URL has expired"} (ถ้าหมดอายุ)
```

**Delete URL:**
```bash
curl -X DELETE http://localhost:8000/my-link \
  -H "Authorization: Bearer <token>"
# 204 No Content (owner only) / 403 Not owner / 404 Not found
```

---

## Rate Limiting

- Sliding window: 100 req / 60s default (configurable via `RATE_LIMIT` env e.g., "50/30")
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 when exceeded: `{"detail": "Rate limit exceeded. Try again in 60 seconds."}`
- Exempt: `/stats/{sid}`, `/health`, `/auth/*`

---

## Tests

| File | Tests | Status |
|------|-------|--------|
| `tests/test_store.py` | 8 tests | ✅ |
| `tests/test_models.py` | 11 tests | ✅ |
| `tests/test_app.py` | 12 tests | ✅ |
| `tests/test_store_sqlite.py` | 19 tests | ✅ |
| `tests/test_rate_limiter.py` | 9 tests | ✅ |
| `tests/test_auth.py` | 13 tests | ✅ |
| `tests/test_custom_id.py` | 22 tests | ✅ |
| `tests/test_expiration.py` | 21 tests | ✅ |
| **Total** | **123 tests** | **✅ All pass** |

---

*Last updated: 2026-09-01*
