# Changelog

> Agentic Demo — Version history
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

---

## [Unreleased]

### Added
- Frontend: login page + custom ID input + TTL picker (v1.0.0 target)
- Analytics dashboard: GET /analytics/{sid} — referrer breakdown, clicks_by_hour, recent_clicks
- Analytics: ReferrerStat, AnalyticsResponse Pydantic models
- Analytics: UrlStore.get_analytics() aggregation method
- Frontend: getAnalytics() client function + 2 tests

### Changed
- Frontend: fixed hydration mismatch by replacing useState+localStorage with useSyncExternalStore
- Frontend: disabled react-hooks/set-state-in-effect rule for mounted guard pattern

### Fixed
- Frontend API test: mock fetch to avoid network dependency in shortenUrl test
- Frontend page: SSR-safe localStorage reads via useSyncExternalStore (no hydration mismatch)
- Frontend: 19/19 tests passing, ESLint clean, tsc clean
- Frontend auth form: mounted guard prevents hydration flash (skeleton until hydrate)
- Frontend auth form: type="button" on Login/Register buttons (prevents accidental form submit)
- Frontend auth form: disabled when email/password empty (prevents double-submit flicker)
- Frontend: 24 tests passing (4 test files), ESLint clean, tsc clean

---

## [1.0.0] - 2026-09-01

### Added
- URL expiration (TTL): `expires_in` field (1–31,536,000 sec), 410 Gone on redirect, `expired` flag + `expires_at` in stats
- DELETE /{sid} endpoint (owner-only, 204/403/404)
- SQLite migration: `expires_at` column with auto-migration
- Custom short ID: `custom_id` field (3–20 chars, `[a-zA-Z0-9_-]+`, reserved path guard: health, stats, docs, redoc, auth, shorten, shorten-anon)
- JWT authentication: register, login, me endpoints; bcrypt password hashing; PyJWT HS256 tokens; UserRepository abstraction (InMemory + SQLite)
- JWT_SECRET, JWT_EXPIRE_MINUTES env vars
- /shorten-anon endpoint (backward compatible, no auth required)
- SQLite persistence: WAL mode, foreign keys, factory pattern via DATABASE_URL
- Rate limiting: sliding window 100 req/60s default, X-RateLimit-* headers, RATE_LIMIT env override (e.g., "50/30"), exempt /stats, /health
- TDD edge cases: duplicate URLs → different short IDs, short_id alphanumeric, click with referrer, stats increment after resolve, model validation
- 123 backend tests + 14 frontend tests (137 total)
- Monorepo migration: backend/ + frontend/ structure
- FastAPI factory `create_app()`, CORS from env, health endpoint
- Next.js 16 API proxy rewrite `/api/* → http://localhost:8000`
- Frontend URL shortener form with shorten/copy/stats UI
- Docker + docker-compose (Python 3.11-slim, Node 22-alpine multi-stage)
- Documentation: API.md, ERROR_HANDLING.md, DATABASE_SCHEMA.md, WORKFLOW.md, AI_PROMPT_TEMPLATE.md
- GitHub Actions CI for dev/qa/sit/uat/main + PRs
- Branch protection: qa=1, sit=1, uat=1, main=2 approvals (human-gated promotion)
- Configurable CORS_ORIGINS, BASE_URL via env
- Pre-commit validation pipeline (6 checks)
- .env.example with BACKEND_HOST/PORT, CORS_ORIGINS, NEXT_PUBLIC_API_URL, DATABASE_URL, RATE_LIMIT

### Changed
- Migrated from Flask to FastAPI (v0.2.0)
- Consolidated docs from PROJECT_DOCS.md to docs/
- Removed auto-promote workflow — switched to human-gated promotion

### Fixed
- Deploy workflow: fixed `python -m pytest tests/` path (working-directory: backend)
- .coverage artifact leak: removed from all env branches, added to .gitignore
- PR #27 merge conflicts: rewrote next.config.ts + page.tsx
- fireEvent.click → fireEvent.submit in jsdom tests
- ruff format + mypy clean on all files

---

## [0.3.0] - 2026-08-31

### Added
- SQLite persistence (WAL mode, urls + clicks tables, factory pattern)
- Rate limiting (sliding window, X-RateLimit headers)
- TDD edge case tests (duplicate URLs, alphanumeric short_id, referrer tracking, stats increment)
- Click analytics (ClickRecord model, history in StatsResponse)

### Changed
- Refactored store layer: UrlStore + SqliteStore abstraction

---

## [0.2.0] - 2026-08-26

### Added
- Pydantic v2 models with type validation
- FastAPI async endpoints (POST /shorten, GET /<id>, GET /stats/<id>)
- Async test client with httpx
- mypy type checking in validation pipeline
- Language-agnostic validation config
- Pre-commit validation pipeline
- Spec intake pipeline with auto-detect
- Project health monitor cron job with continuity
- Best practices registry

### Changed
- Migrated from Flask to FastAPI
- Validation config now auto-detects project language

---

## [0.1.0] - 2026-08-26

### Added
- Initial Flask URL shortener implementation
- In-memory URL store with click tracking
- Basic test suite (pytest)
- Linting with ruff
- Git repository setup with conventional commits

---

*Last updated: 2026-09-01*