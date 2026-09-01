# Feature: Rate Limiting

priority: P1
status: ready
created: 2026-08-31
author: ai-generated

## User Story
As a system owner, I want rate limiting on API endpoints so that abuse and excessive requests are prevented.

## UI Mockup
N/A — backend only. Returns HTTP 429 when exceeded.

## API Contract

### Endpoint: `POST /shorten`
```
Headers:
  X-RateLimit-Limit: 100        (requests per window)
  X-RateLimit-Remaining: 99     (remaining)
  X-RateLimit-Reset: 1693500000 (unix timestamp)

Response 429:
  { "detail": "Rate limit exceeded. Try again in 60 seconds." }
```

### Endpoint: `GET /<short_id>` (redirect)
Same headers. Returns 429 if exceeded.

### Endpoint: `GET /stats/{short_id}`
No rate limit (read-only, low cost).

## Acceptance Criteria
- [ ] AC-1: Given default config, when POST /shorten is called 101 times in 60s window, then 101st returns 429
- [ ] AC-2: Given rate limit headers present, when request succeeds, then X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset are set
- [ ] AC-3: Given RATE_LIMIT=50 env, when 51st POST /shorten in window, then 429 returned
- [ ] AC-4: Given rate limit exceeded, when 60s window resets, then next request succeeds
- [ ] AC-5: Given rate limit on /<id> redirect, when exceeded, then 429 returned
- [ ] AC-6: Given GET /stats/{sid}, when called many times, then no rate limit applied

## Store Changes
| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| check | `rate_limiter.check(key)` | `str` | `bool` (True=allowed) |
| get info | `rate_limiter.info(key)` | `str` | `RateLimitInfo` |

## Files to Modify
- [ ] `backend/src/rate_limiter.py` — new RateLimiter class (in-memory sliding window)
- [ ] `backend/src/config.py` — add RATE_LIMIT, RATE_LIMIT_WINDOW env
- [ ] `backend/src/app.py` — apply to POST /shorten and GET /<id>
- [ ] `backend/tests/test_rate_limiter.py` — unit tests
- [ ] `backend/tests/test_app.py` — integration tests for 429

## TDD Checklist
- [ ] Write failing tests first (RED)
- [ ] Minimal implementation (GREEN)
- [ ] Refactor (REFACTOR)
- [ ] All quality gates pass

## Out of Scope
- Redis-backed rate limiting
- Per-user authentication-based limits
- Rate limit bypass tokens
