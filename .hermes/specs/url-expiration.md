# Feature: URL Expiration (TTL)

priority: P2
status: ready
created: 2026-09-01

## User Story
As a user, I want my short URLs to expire automatically after a set time, so that temporary links don't live forever.

## API

```json
// POST /shorten
{
  "url": "https://example.com",
  "custom_id": "my-link",       // optional
  "expires_in": 3600            // optional, seconds (1 - 31536000 = 1 year)
}

// Response (ShortenResponse)
// { "short_id": "my-link", "short_url": "...", "expires_at": "2026-09-01T10:00:00Z" }

// GET /{sid}
-- 307 if not expired
-- 410 Gone if expired (JSON body: { detail: "Short URL has expired" })

// GET /stats/{sid}
-- Returns expired: true/false + expires_at

// DELETE /{sid}  (authenticated, owner only)
-- Deletes URL (204)
-- 404 if not found, 403 if not owner, 401 if not authenticated
```

## Validation Rules

| Field | Rule |
|-------|------|
| `expires_in` | 1 – 31536000 (1 year), integer |
| `expires_at` | auto-computed from expires_in |
| Default | `null` = never expires |
| Expired check | `datetime.now(timezone.utc) > expires_at` |

## Storage

- `urls.expires_at TEXT NULL` column (ISO8601 UTC)
- `peek()` returns tuple or includes expiry check
- `resolve()` returns None + 410 handling in app layer

## TDD Steps

1. Add `expires_in` to ShortenRequest, validation
2. Add `expires_at` to ShortenResponse
3. Update UrlStore / SqliteStore to store + check expiry
4. Update app.py routes to handle expiry
5. Add tests: valid TTL, invalid, expiry redirect 410, stats expired flag
6. Add DELETE endpoint for cleanup
