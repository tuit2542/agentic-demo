# Agent Instructions

## Tech Stack
- Python 3.11, Flask 3.x, pytest, ruff

## Commands
- Test: `pytest tests/ -v`
- Lint: `ruff check src/ tests/`
- Auto-fix: `ruff check --fix src/ tests/`

## Rules
- TDD: write failing test first, then minimal implementation
- Conventional Commits: `feat:`, `fix:`, `chore:`
- No wildcard imports
- Type hints on all public functions
- Run lint + tests before every commit
