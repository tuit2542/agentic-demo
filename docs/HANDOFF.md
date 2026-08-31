# Context Handoff

> สำหรับ AI session ใหม่ — อ่านไฟล์นี้ก่อนเริ่มงาน

---

## Current State (2026-08-31)

### Project
- **Repo:** https://github.com/tuit2542/agentic-demo
- **Structure:** Monorepo (backend/ + frontend/)
- **Backend:** Python 3.11, FastAPI, Pydantic v2, uvicorn
- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS
- **Branching:** feat/* → dev → qa → sit → uat → main (auto-promote)

### What's Done
| # | Feature | Status |
|---|---------|--------|
| 1 | URL Shortener API (FastAPI) | ✅ |
| 2 | Pydantic models | ✅ |
| 3 | In-memory store | ✅ |
| 4 | 16 backend tests (pytest) | ✅ |
| 5 | 4 frontend tests (Vitest) | ✅ |
| 6 | CORS middleware | ✅ |
| 7 | Next.js API proxy | ✅ |
| 8 | Frontend URL shortener page | ✅ |
| 9 | Pre-commit validation (6 checks) | ✅ |
| 10 | GitHub Actions CI | ✅ |
| 11 | Auto-promote workflow | ✅ |
| 12 | Branch protection (5 branches) | ✅ |
| 13 | Docker + docker-compose | ✅ |
| 14 | Documentation (docs/) | ✅ |
| 15 | AI tracking checklist | ✅ |

### Pending
| # | Feature | Priority |
|---|---------|----------|
| 1 | SQLite/PostgreSQL storage | 🔴 High |
| 2 | Rate limiting | 🔴 High |
| 3 | JWT authentication | 🟡 Medium |
| 4 | Custom short ID | 🟡 Medium |
| 5 | URL expiration | 🟡 Medium |
| 6 | Click analytics | 🟢 Low |

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
| Tests | `pytest tests/ -v` | ✅ |
| Frontend lint | `npm run lint` | ✅ |
| Frontend type | `npx tsc --noEmit` | ✅ |
| Frontend test | `npm run test` | ✅ |

---

## Branch Structure

```
main (prod) ← 2 approvals
  └── uat ← 1 approval
        └── sit ← 1 approval
              └── qa ← 1 approval
                    └── dev ← 1 approval
                          └── feat/* (auto-promote)
```

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

---

*Last updated: 2026-08-31*
