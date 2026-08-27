# Agent Instructions

## Tech Stack
- Python 3.11, FastAPI 0.110+ (async), Pydantic v2, uvicorn
- Testing: pytest + pytest-asyncio + httpx
- Linting: ruff
- Type checking: mypy
- Security: pip-audit

## Commands
- Test: `pytest tests/ -v`
- Lint: `ruff check src/ tests/`
- Format: `ruff format src/ tests/`
- Type check: `mypy src/ --ignore-missing-imports`
- Security: `pip-audit --desc`
- Validate all: `python scripts/pre_commit_validate.py`

## Rules
- TDD: write failing test first, then minimal implementation
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `ci:`
- No wildcard imports
- Type hints on all public functions
- Pydantic models for all request/response
- Use `from __future__ import annotations`
- Run full validation pipeline before every commit

## Quality Gates
| Gate | Must Pass |
|------|-----------|
| Lint (ruff) | ✅ |
| Format (ruff format) | ✅ |
| Type check (mypy) | ✅ |
| Tests (pytest) | ✅ |
| Security (pip-audit) | ⚠️ warn-only |

## Auto-Update Documentation
After completing any task, update relevant docs in `docs/`:
1. **docs/API.md** — New API endpoints, models, store methods
2. **docs/CHANGELOG.md** — New features under [Unreleased]
3. **docs/HANDOFF.md** — Current state, pending items
4. **docs/WORKFLOW.md** — Flow/branching changes
5. **docs/INDEX.md** — Diagram changes
