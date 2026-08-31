# Feature: Click Analytics

priority: P1
status: draft
created: 2026-08-31
author: ai-generated

## User Story
As a user, I want to see detailed click analytics for my short URLs so that I can track usage patterns.

## Acceptance Criteria

### AC-1: Basic click count (existing)
- Given a short URL with 5 clicks
- When I GET /stats/{sid}
- Then I see clicks: 5

### AC-2: Click history with timestamps
- Given a short URL with 3 clicks at different times
- When I GET /stats/{sid}
- Then I see a clicks_history array with 3 entries, each having a timestamp

### AC-3: Click by hour breakdown
- Given a short URL with 10 clicks spread across hours
- When I GET /stats/{sid}?group_by=hour
- Then I see clicks grouped by hour

### AC-4: Click by date breakdown
- Given a short URL with clicks over 3 days
- When I GET /stats/{sid}?group_by=date
- Then I see clicks grouped by date

### AC-5: Stats response format
- When I GET /stats/{sid}
- Then response contains: short_id, original_url, clicks, clicks_history

## API Contract

### Endpoint: `GET /stats/{sid}`
```
Response 200:
{
  "short_id": "AbC123",
  "original_url": "https://example.com",
  "clicks": 5,
  "clicks_history": [
    {"timestamp": "2026-08-31T10:00:00Z", "referrer": null}
  ]
}

Response 404:
{
  "detail": "Short URL not found"
}
```

### Updated Models
```python
class ClickRecord(BaseModel):
    timestamp: str
    referrer: str | None = None

class StatsResponse(BaseModel):
    short_id: str
    clicks: int
    original_url: str
    clicks_history: list[ClickRecord]
```

## Store Changes

| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| Add click record | `store.record_click(sid)` | `str` | `ClickRecord` |
| Get history | `store.get_history(sid)` | `str` | `list[ClickRecord]` |

## Files to Modify
- [ ] `backend/src/models.py` — add ClickRecord, update StatsResponse
- [ ] `backend/src/store.py` — add clicks_history, record_click, get_history
- [ ] `backend/src/app.py` — update stats endpoint to return history
- [ ] `backend/tests/test_models.py` — ClickRecord tests
- [ ] `backend/tests/test_store.py` — history tests
- [ ] `backend/tests/test_app.py` — stats endpoint tests

## TDD Checklist
- [ ] Write failing tests first (RED)
- [ ] Minimal implementation (GREEN)
- [ ] Refactor (REFACTOR)
- [ ] All quality gates pass

## Out of Scope
- Click by referrer analysis (future feature)
- Geographic click data
- Real-time analytics dashboard
