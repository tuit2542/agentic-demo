# Feature: Password-Protected Links

<!-- spec_id: password-protected-links -->
priority: P1
status: ready
created: 2026-09-07
author: ai-generated

## User Story
As a logged-in user, I want to protect my short links with a password so that only people who know the password can access the original URL.

## API Contract

### Endpoint: `POST /shorten` (extended)
```
Request:
  Body: { "url": "https://example.com", "password": "secret123" }  // password optional, 4-64 chars

Response 201:
  { "short_id": "abc", "short_url": "http://localhost:8000/abc", "expires_at": null, "is_protected": true }

Response 422:
  { "detail": "Password must be 4-64 characters" }
```

### Endpoint: `GET /{sid}` (modified)
```
If link has password and no/wrong password supplied:
  Response 401: { "detail": "Password required" } or { "detail": "Invalid password" }
If password correct via ?password=... or header X-Link-Password:
  Response 307 → original URL

Response 410: { "detail": "Short URL has expired" }
Response 404: { "detail": "Short URL not found" }
```

### Pydantic Models
```python
class ShortenRequest(BaseModel):
    url: str
    custom_id: str | None = None
    expires_in: int | None = None
    password: str | None = None  # 4-64 chars if provided

class ShortenResponse(BaseModel):
    short_id: str
    short_url: str
    expires_at: str | None
    is_protected: bool = False

class VerifyPasswordRequest(BaseModel):
    password: str
```

## Acceptance Criteria

- [ ] AC-1: Given a user creates a link with password, when GET /{sid} without password, then returns 401 "Password required"
- [ ] AC-2: Given a password-protected link, when GET /{sid}?password=correct, then returns 307 redirect
- [ ] AC-3: Given a password-protected link, when GET /{sid}?password=wrong, then returns 401 "Invalid password"
- [ ] AC-4: Given a normal link (no password), when GET /{sid}, then returns 307 directly (no regression)
- [ ] AC-5: Given password too short/long, when POST /shorten with password, then returns 422

## Store Changes

| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| create with password | `store.shorten(url, ..., password?)` | `str | None` | hash stored |
| check password | `store.verify_password(sid, password)` | `str, str` | `bool` |
| get protected status | stored in `_password_hash: dict[str, str]` + DB column `password_hash TEXT` | — | — |

## Files to Modify

- [ ] `backend/src/models.py` — add password validator + is_protected field
- [ ] `backend/src/store.py` — add password_hash handling
- [ ] `backend/src/store_sqlite.py` — add password_hash column
- [ ] `backend/src/app.py` — modify POST /shorten + GET /{sid}
- [ ] `frontend/src/lib/api.ts` — add password param
- [ ] `frontend/src/app/page.tsx` — add password input
- [ ] `frontend/src/app/p/[sid]/page.tsx` — password prompt page
