# Feature: Analytics Dashboard

priority: P1
status: ready
created: 2026-09-01

## User Story
As a user, I want to see click analytics for my short URLs — referrer breakdown, time-based trends, and click history — so that I can understand where my traffic comes from.

## API Contract

### Endpoint: `GET /analytics/{sid}`
```
Response 200:
{
  "short_id": "abc123",
  "total_clicks": 42,
  "unique_referrers": 5,
  "top_referrers": [
    { "referrer": "https://twitter.com", "count": 18 },
    { "referrer": "https://facebook.com", "count": 12 },
    { "referrer": null, "count": 8 },
    { "referrer": "https://github.com", "count": 4 }
  ],
  "clicks_by_hour": {
    "2026-09-01T08:00:00Z": 5,
    "2026-09-01T09:00:00Z": 12,
    "2026-09-01T10:00:00Z": 25
  },
  "recent_clicks": [
    { "timestamp": "2026-09-01T10:30:00Z", "referrer": "https://twitter.com" }
  ],
  "expired": false,
  "expires_at": "2026-09-08T10:00:00Z"
}

Response 404:
  { "detail": "Short URL not found" }
```

### Pydantic Models
```python
class ReferrerStat(BaseModel):
    referrer: str | None
    count: int

class AnalyticsResponse(BaseModel):
    short_id: str
    total_clicks: int
    unique_referrers: int
    top_referrers: list[ReferrerStat]
    clicks_by_hour: dict[str, int]
    recent_clicks: list[ClickRecord]
    expired: bool = False
    expires_at: str | None = None
```

## Acceptance Criteria
- [ ] AC-1: Given a valid short_id with clicks, when GET /analytics/{sid}, then returns total_clicks, referrer breakdown, clicks_by_hour
- [ ] AC-2: Given a valid short_id with no clicks, when GET /analytics/{sid}, then returns total_clicks=0 with empty referrers
- [ ] AC-3: Given a non-existent short_id, when GET /analytics/{sid}, then returns 404
- [ ] AC-4: Given clicks with mixed referrers (some null), when GET /analytics/{sid}, then unique_referrers counts non-null referrers only
- [ ] AC-5: Given clicks within the same hour, when GET /analytics/{sid}, then clicks_by_hour groups them correctly

## Store Changes
| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| read | `store.get_analytics(sid)` | `str` | `AnalyticsData` (dataclass) |

## Files to Modify
- [ ] `backend/src/models.py` — add ReferrerStat, AnalyticsResponse
- [ ] `backend/src/store.py` — add get_analytics() method
- [ ] `backend/src/store_sqlite.py` — add get_analytics() method
- [ ] `backend/src/app.py` — add GET /analytics/{sid} endpoint
- [ ] `backend/tests/test_analytics.py` — analytics tests (RED→GREEN→REFACTOR)
- [ ] `frontend/src/app/page.tsx` — analytics card UI
- [ ] `frontend/src/lib/api.ts` — getAnalytics() client function
- [ ] `frontend/src/__tests__/api.test.ts` — getAnalytics tests

## TDD Checklist
- [ ] Write failing tests first (RED)
- [ ] Minimal implementation (GREEN)
- [ ] Refactor (REFACTOR)
- [ ] All quality gates pass

## Out of Scope
- Real-time WebSocket updates
- CSV/PDF export
- Date range filtering (future enhancement)
- Geographic analytics
