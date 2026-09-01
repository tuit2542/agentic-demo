# Context Handoff

> สำหรับ AI session ใหม่ — อ่านไฟล์นี้ก่อนเริ่มงาน

---

## Current State (2026-08-31)

### Project
- **Repo:** https://github.com/tuit2542/agentic-demo
- **Structure:** Monorepo (backend/ + frontend/)
- **Backend:** Python 3.11, FastAPI, Pydantic v2, uvicorn
- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS
- **Branching:** feat/* → dev → qa → sit → uat → main (human-gated promotion)

### What's Done
| # | Feature | Tests |
|---|---------|-------|
| 1 | URL Shortener API (FastAPI) | ✅ |
| 2 | Pydantic models + validation | ✅ |
| 3 | In-memory store | ✅ |
| 4 | 34 backend tests (pytest) | ✅ |
| 5 | 14 frontend tests (Vitest) | ✅ |
| 6 | CORS middleware (configurable) | ✅ |
| 7 | Next.js API proxy | ✅ |
| 8 | Frontend URL shortener page | ✅ |
| 9 | Pre-commit validation (6 checks) | ✅ |
| 10 | GitHub Actions CI (backend + frontend) | ✅ |
| 11 | Branch protection (qa/sit/uat/main) | ✅ |
| 12 | Docker + docker-compose | ✅ |
| 13 | Documentation (docs/) | ✅ |
| 14 | AI tracking checklist | ✅ |
| 15 | Configurable CORS + base URL | ✅ |
| 16 | Frontend validation script | ✅ |
| 17 | Click analytics tracking | ✅ |
| 18 | TDD edge case tests (34+14) | ✅ |
| 19 | Deployment workflow | ✅ |

### Pending
| # | Feature | Priority | Spec |
|---|---------|----------|------|
| 1 | SQLite/PostgreSQL storage | 🔴 High | ยังไม่มี spec |
| 2 | Rate limiting | 🔴 High | ยังไม่มี spec |
| 3 | JWT authentication | 🟡 Medium | ยังไม่มี spec |
| 4 | Custom short ID | 🟡 Medium | ยังไม่มี spec |
| 5 | URL expiration | 🟡 Medium | ยังไม่มี spec |

> ยังไม่มี feature spec สำหรับ pending items — สร้างจาก `.hermes/specs/TEMPLATE.md`

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

---

## Quality Gates

| Check | Command | Status |
|-------|---------|--------|
| Lint | `ruff check src/ tests/` | ✅ |
| Format | `ruff format --check src/ tests/` | ✅ |
| Type check | `mypy src/ --ignore-missing-imports` | ✅ |
| Tests | `pytest tests/ -v` | ✅ (34 passed) |
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
                    └── dev
                          └── feat/* (PR → dev only)
```

**Agent scope:** PR → dev only. Humans handle promotion.

---

## How to Continue

### New Feature
```bash
git checkout dev && git pull
git checkout -b feat/my-feature
# 1. Read docs/TRACKING.md
# 2. Copy .hermes/specs/TEMPLATE.md → fill spec
# 3. TDD: RED → GREEN → REFACTOR
# 4. Validate → Commit → Push → Create PR to dev
```

### Bug Fix
```bash
git checkout -b fix/my-bug
# Fix + test + validate + commit
```

---

## Key Files

1. `AGENTS.md` — Agent rules + commands
2. `docs/TRACKING.md` — Feature checklist
3. `docs/ERROR_HANDLING.md` — Error patterns
4. `docs/DATABASE_SCHEMA.md` — Data layer
5. `docs/API.md` — API reference
6. `.hermes/specs/TEMPLATE.md` — Spec template
7. `backend/.hermes.md` — Backend-specific rules
8. `frontend/.hermes.md` — Frontend-specific rules

---

*Last updated: 2026-08-31*
