# Context Handoff

> สำหรับ AI session ใหม่ — อ่านไฟล์นี้ก่อนเริ่มงาน

---

## Current State (2026-09-01)

### Project
- **Repo:** https://github.com/tuit2542/agentic-demo
- **Structure:** Monorepo (backend/ + frontend/)
- **Backend:** Python 3.11, FastAPI, Pydantic v2, uvicorn, SQLite (WAL), bcrypt, PyJWT
- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS
- **Branching:** feat/* → dev → qa → sit → uat → main (human-gated promotion)
- **Tags:** v0.1.0 → v0.6.0

### What's Done (v0.6.0 — 123 backend + 14 frontend tests)

| # | Feature | Status |
|---|---------|--------|
| 1 | FastAPI URL Shortener (POST /shorten, GET /{sid}, GET /stats/{sid}) | ✅ |
| 2 | Pydantic v2 models (validation: url, email, password, custom_id, expires_in) | ✅ |
| 3 | In-memory UrlStore | ✅ |
| 4 | SQLite persistence (WAL mode, auto-migrate, factory via DATABASE_URL) | ✅ |
| 5 | JWT auth (register/login/me, bcrypt, HTTPBearer, get_user_repo singleton) | ✅ |
| 6 | Custom short ID (3-20 chars, [a-zA-Z0-9_-]+, reserved path guard) | ✅ |
| 7 | URL expiration (expires_in 1-31536000s, 410 Gone, expired flag in stats) | ✅ |
| 8 | DELETE /{sid} (owner-only, 204/403/404) | ✅ |
| 9 | Rate limiting (sliding window 100/60s, X-RateLimit-* headers, RATE_LIMIT env) | ✅ |
| 10 | /shorten-anon (backward compatible, no auth required) | ✅ |
| 11 | TDD edge cases (duplicate, alphanumeric, long URL, referrer, history order) | ✅ |
| 12 | Frontend page (URL shortener form, 14 tests) | ✅ |
| 13 | Docker + docker-compose | ✅ |
| 14 | GitHub Actions CI (backend + frontend) | ✅ |
| 15 | Branch protection (qa=1, sit=1, uat=1, main=2 approvals) | ✅ |
| 16 | Configurable CORS + base URL + JWT secret (env) | ✅ |
| 17 | Pre-commit validation pipeline | ✅ |

### Pending
| # | Feature | Priority | Spec |
|---|---------|----------|------|
| 1 | Frontend: login + custom ID + TTL picker | 🟡 Medium | ยังไม่มี spec |
| 2 | JWT refresh token | 🟢 Low | ยังไม่มี spec |
| 3 | Analytics dashboard | 🟢 Low | ยังไม่มี spec |
| 4 | URL bulk import | 🟢 Low | ยังไม่มี spec |

---

## Quick Start

```bash
# Docker
docker-compose up --build

# Manual
cd backend && python -m uvicorn src.app:create_app --factory --reload
cd frontend && npm run dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Auth example
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Login → get JWT
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Create short URL (with auth)
curl -X POST http://localhost:8000/shorten \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_id": "my-link", "expires_in": 3600}'
```

---

## Quality Gates

| Check | Command | Status |
|-------|---------|--------|
| Lint | `ruff check src/ tests/` | ✅ |
| Format | `ruff format --check src/ tests/` | ✅ |
| Type check | `mypy src/` | ✅ |
| Tests | `pytest tests/ -q` | ✅ (123 passed) |
| Frontend lint | `npm run lint` | ✅ |
| Frontend type | `npx tsc --noEmit` | ✅ |
| Frontend test | `npm run test` | ✅ (14 passed) |

---

## Branch Structure

```
main (prod) ← 2 approvals
  └── uat ← 1 approval
        └── sit ← 1 approval
              └── qa ← 1 approval
                    └── dev ← CI pass only
                          └── feat/* (PR → dev only)
```

**Agent scope:** PR → dev only. Humans handle promotion.

---

## Key Files

| # | File | Purpose |
|---|------|---------|
| 1 | `AGENTS.md` | Agent rules + commands |
| 2 | `docs/TRACKING.md` | Feature checklist |
| 3 | `docs/WORKFLOW.md` | Mermaid flowchart of Agent vs Human |
| 4 | `docs/API.md` | API reference |
| 5 | `docs/DATABASE_SCHEMA.md` | Data layer |
| 6 | `.hermes/specs/TEMPLATE.md` | Spec template |
| 7 | `backend/.hermes.md` | Backend-specific rules |
| 8 | `frontend/.hermes.md` | Frontend-specific rules |

---

*Last updated: 2026-09-01*
