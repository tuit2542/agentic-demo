# Agent Instructions

## Monorepo Structure
- `backend/` — Python FastAPI (src/, tests/, scripts/)
- `frontend/` — Next.js 16 + React 19 + TypeScript
- `docs/` — Documentation

## Backend Tech Stack
- Python 3.11, FastAPI 0.110+ (async), Pydantic v2, uvicorn
- Testing: pytest + pytest-asyncio + httpx
- Linting: ruff
- Type checking: mypy
- Security: pip-audit

## Frontend Tech Stack
- Next.js 16, React 19, TypeScript, Tailwind CSS
- Testing: Vitest + React Testing Library
- Linting: ESLint (eslint-config-next)
- Type checking: TypeScript (tsc)

## Commands

### Backend
- Test: `cd backend && pytest tests/ -v`
- Lint: `cd backend && ruff check src/ tests/`
- Format: `cd backend && ruff format src/ tests/`
- Type check: `cd backend && mypy src/ --ignore-missing-imports`
- Security: `cd backend && pip-audit --desc`
- Validate all: `cd backend && python scripts/pre_commit_validate.py`

### Frontend
- Dev: `cd frontend && npm run dev`
- Build: `cd frontend && npm run build`
- Test: `cd frontend && npm run test`
- Lint: `cd frontend && npm run lint`
- Type check: `cd frontend && npx tsc --noEmit`

## Rules
- TDD: write failing test first, then minimal implementation
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `ci:`
- No wildcard imports
- Type hints on all public functions (backend)
- Pydantic models for all request/response (backend)
- Use `from __future__ import annotations` (backend)
- Prefer Server Components, use 'use client' only when needed (frontend)
- All components must have tests (frontend)
- Run full validation pipeline before every commit

## Quality Gates
| Gate | Backend | Frontend |
|------|---------|----------|
| Lint | ruff ✅ | ESLint ✅ |
| Format | ruff format ✅ | - (not configured) |
| Type check | mypy ✅ | tsc ✅ |
| Tests | pytest ✅ | Vitest ✅ |
| Security | pip-audit ⚠️ | npm audit ⚠️ |

## Branching & Promotion

```
feat/* → dev → qa → sit → uat → main
```

| Promotion | Policy |
|-----------|--------|
| feat → dev | CI pass only |
| dev → qa | CI pass only |
| qa → sit | 1 approval required |
| sit → uat | 1 approval required |
| uat → main | 2 approvals required |

**Agent responsibility:** Create PR → target `dev`. Done. Humans handle promotion.

## Feature Spec Template
When starting a new feature, copy `.hermes/specs/TEMPLATE.md` and fill in:
- User Story + Acceptance Criteria (Given/When/Then format)
- UI Mockup (paste image path — AI follows layout)
- API Contract + Pydantic Models
- Store Changes + Files to Modify
- TDD Checklist

## Error Handling Rules
- Always use `HTTPException` with `detail` field
- Status codes: 200, 201, 307, 404, 422, 429, 500
- Never expose internals in responses
- Test all error paths
- Reference: `docs/ERROR_HANDLING.md`

## Database Schema
- Current: In-memory dict (see `backend/src/store.py`)
- BaseStore interface methods: `shorten(url)`, `resolve(short_id)`, `stats(short_id)`
- Future: SQLite → PostgreSQL (see `docs/DATABASE_SCHEMA.md`)

## Auto-Update Documentation
After completing any task, update relevant docs in `docs/`:
1. **API.md** — Add new endpoint row to `Endpoints` table + add example
2. **CHANGELOG.md** — Add bullet under `## [Unreleased]`
3. **HANDOFF.md** — Update `What's Done` table + `Current State` date
4. **TRACKING.md** — Mark completed items in checklist

## Changelog Rule (ENFORCED BY CI)
- Every `feat:` or `fix:` commit MUST have a changelog entry
- Add entry under `## [Unreleased]` in `docs/CHANGELOG.md`
- Format: `- Description of change`
- Run `cd backend && python scripts/check_changelog.py` to verify
- Commit WILL FAIL if changelog not updated (validation pipeline blocks it)

## Feature Tracking
- Read `docs/TRACKING.md` before starting any new feature
- Follow the checklist step by step
