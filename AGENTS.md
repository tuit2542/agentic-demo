# Agent Instructions

## Project Goal
> ✏️ **เปลี่ยนตรงนี้** — ใส่เป้าหมายโปรเจคของคุณ เช่น "Todo App", "Blog Platform" ฯลฯ
>
> ตัวอย่าง: Build a URL Shortener monorepo that proves AI agents can execute full-loop engineering independently.

---

## Monorepo Structure
- `backend/` — Python FastAPI (src/, tests/, scripts/)
- `frontend/` — Next.js + React + TypeScript
- `docs/` — Documentation

## Backend Tech Stack
- Python 3.11, FastAPI (async), Pydantic v2, uvicorn
- Testing: pytest + httpx
- Linting: ruff
- Type checking: mypy
- Security: pip-audit

## Frontend Tech Stack
- Next.js, React, TypeScript, Tailwind CSS
- Testing: Vitest + React Testing Library
- Linting: ESLint
- Type checking: TypeScript (tsc)

## Commands

### Backend
| Action | Command |
|--------|---------|
| Test | `cd backend && pytest tests/ -v` |
| Lint | `cd backend && ruff check src/ tests/` |
| Format | `cd backend && ruff format src/ tests/` |
| Type check | `cd backend && mypy src/ --ignore-missing-imports` |
| Validate all | `cd backend && python scripts/pre_commit_validate.py` |

### Frontend
| Action | Command |
|--------|---------|
| Dev | `cd frontend && npm run dev` |
| Build | `cd frontend && npm run build` |
| Test | `cd frontend && npm run test` |
| Lint | `cd frontend && npm run lint` |
| Type check | `cd frontend && npx tsc --noEmit` |

## Rules
- **TDD:** Write failing test first → minimal implementation → refactor
- **Conventional Commits:** `feat:`, `fix:`, `chore:`, `docs:`, `ci:`
- **No wildcard imports**
- **Type hints** on all public functions (backend)
- **Pydantic models** for all request/response (backend)
- **Use `from __future__ import annotations`** (backend)
- **Prefer Server Components**, use 'use client' only when needed (frontend)
- **All components must have tests** (frontend)
- **Full validation pipeline** before every commit

## Quality Gates

| Gate | Backend | Frontend |
|------|---------|----------|
| Lint | `ruff check` | ESLint |
| Type | mypy | tsc |
| Tests | pytest | vitest |
| Security | pip-audit | npm audit |

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

**Agent responsibility:** Create PR → target `dev`. Done.  
**Human responsibility:** Handle promotion (dev → qa → sit → uat → main).

## Feature Spec Template
When starting a new feature, copy `.hermes/specs/TEMPLATE.md` and fill in:
- User Story + Acceptance Criteria (Given/When/Then format)
- API Contract + Pydantic Models
- Store Changes + Files to Modify
- TDD Checklist

## Error Handling Rules
- Always use `HTTPException` with `detail` field
- Status codes: 200, 201, 307, 404, 422, 429, 500
- Never expose internals in responses
- Test all error paths

## Auto-Update Documentation
After completing any task, update relevant docs in `docs/`:
1. **CHANGELOG.md** — Add bullet under `## [Unreleased]`
2. **API.md** — Add new endpoint row + example
3. **HANDOFF.md** — Update `What's Done` table + `Current State`

## Changelog Rule (ENFORCED BY CI)
- Every `feat:` or `fix:` commit MUST have a changelog entry
- Add entry under `## [Unreleased]` in `docs/CHANGELOG.md`
- Format: `- Description of change`
- Commit WILL FAIL if changelog not updated

## Feature Tracking
- Read `docs/TRACKING.md` before starting any new feature
- Follow the checklist step by step
