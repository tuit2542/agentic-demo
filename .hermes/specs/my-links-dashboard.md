# Feature: My Links Dashboard

<!-- spec_id: my-links-dashboard -->
priority: P1
status: ready
created: 2026-09-07
author: ai-generated

## User Story
As a logged-in user, I want to see all my shortened URLs in one dashboard so that I can manage, monitor, and delete my links easily.

## API Contract

### Endpoint: `GET /my/urls`
```
Headers:
  Authorization: Bearer <token>

Response 200:
  {
    "urls": [
      {
        "short_id": "my-link",
        "original_url": "https://example.com",
        "short_url": "http://localhost:8000/my-link",
        "clicks": 5,
        "expired": false,
        "expires_at": "2026-09-10T10:00:00Z",
        "created_at": "2026-09-07T10:00:00Z"
      }
    ],
    "total": 1
  }

Response 401:
  { "detail": "Not authenticated" }
```

### Pydantic Models
```python
class UserUrlItem(BaseModel):
    short_id: str
    original_url: str
    short_url: str
    clicks: int
    expired: bool
    expires_at: str | None
    created_at: str

class UserUrlsResponse(BaseModel):
    urls: list[UserUrlItem]
    total: int
```

## Acceptance Criteria

- [ ] AC-1: Given a logged-in user with 3 URLs, when GET /my/urls, then returns 3 items with correct fields
- [ ] AC-2: Given no auth token, when GET /my/urls, then returns 401
- [ ] AC-3: Given a logged-in user, when GET /my/urls, then only their own URLs are returned (not other users')
- [ ] AC-4: Given URLs with various states, when GET /my/urls, then expired/expiring/active status is correct
- [ ] AC-5: Given a logged-in user, when they click "delete" on a link, then the link is removed from the list

## Store Changes

| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| list_by_owner | `store.list_by_owner(user_id)` | `int` | `list[dict]` with short_id, url, clicks, expired, expires_at, created_at |

## Files to Modify

- [ ] `backend/src/models.py` — add UserUrlItem, UserUrlsResponse
- [ ] `backend/src/store.py` — add list_by_owner() to UrlStore + BaseStore
- [ ] `backend/src/app.py` — add GET /my/urls
- [ ] `backend/tests/test_models.py` — model tests
- [ ] `backend/tests/test_store.py` — store tests
- [ ] `backend/tests/test_app.py` — endpoint tests
- [ ] `frontend/src/lib/api.ts` — add getUserUrls()
- [ ] `frontend/src/app/dashboard/page.tsx` — dashboard page
- [ ] `frontend/src/__tests__/dashboard.test.tsx` — dashboard tests
