# Feature: Custom Short ID

priority: P2
status: ready
created: 2026-09-01

## User Story
As a user, I want to create short URLs with a custom alias so that the resulting link is more memorable and brandable.

## Acceptance Criteria
- User can pass `custom_id` (3-20 chars, alphanumeric + hyphens + underscores)
- Validation: `[a-zA-Z0-9_-]{3,20}`
- Reject reserved paths: `health`, `stats`, `docs`, `redoc`, `auth`, `shorten`, `shorten-anon`
- Reject duplicates: `409 Conflict` if custom_id already taken
- Without `custom_id`: auto-generate (backward compatible)
- Custom ID links are fully functional (redirect, stats, click tracking)

## API Changes
```json
// POST /shorten
{
  "url": "https://example.com",
  "custom_id": "my-brand"   // optional, new field
}
```

## Validation Rules
| Rule | Value |
|------|-------|
| Length | 3-20 chars |
| Pattern | `^[a-zA-Z0-9_-]+$` |
| Reserved | `health, stats, docs, redoc, auth, shorten, shorten-anon` |
| Duplicate | 409 Conflict |

## TDD Steps
1. Add `custom_id: str | None = None` field to `ShortenRequest`
2. Write tests: valid custom ID, invalid (too short/special chars), reserved, duplicate
3. Update `UrlStore.shorten()` and `SqliteStore.shorten()` to accept optional custom_id
4. Update `app.py` /shorten route to handle custom_id
5. Validate all, run CI, promote
