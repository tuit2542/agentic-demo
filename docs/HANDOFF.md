# Context Handoff

> สำหรับ AI session ใหม่ — อ่านไฟล์นี้ก่อนเริ่มงาน

---

## Current State (2026-08-27)

### Project
- **Repo:** https://github.com/tuit2542/agentic-demo
- **Branch:** main (protected, 2 approvals)
- **Last commit:** chore: improve quality gates
- **Tags:** v0.1.0, v0.2.0

### What's Done

| # | Feature | Status |
|---|---------|--------|
| 1 | URL Shortener API (FastAPI) | ✅ |
| 2 | Pydantic models | ✅ |
| 3 | In-memory store | ✅ |
| 4 | 16 tests passing | ✅ |
| 5 | Pre-commit validation (5 checks) | ✅ |
| 6 | Language-agnostic validation | ✅ |
| 7 | Spec intake pipeline | ✅ |
| 8 | Health monitor cron | ✅ |
| 9 | GitHub Actions CI | ✅ |
| 10 | Auto-promote workflow | ✅ |
| 11 | Deploy workflow | ✅ |
| 12 | Branch protection (5 branches) | ✅ |
| 13 | Enterprise branching strategy | ✅ |
| 14 | PR creation skill | ✅ |
| 15 | Documentation (docs/) | ✅ |
| 16 | Best practices registry | ✅ |
| 17 | SOUL.md (global) | ✅ |
| 18 | Test coverage tracking (98%) | ✅ |
| 19 | Code format (ruff format) | ✅ |
| 20 | PR template | ✅ |
| 21 | CODEOWNERS | ✅ |
| 22 | Best practices auto-check (CI) | ✅ |
| 23 | .editorconfig | ✅ |

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

## Quality Gates

| Check | Command | Must Pass |
|-------|---------|-----------|
| Lint | `ruff check src/ tests/` | ✅ |
| Format | `ruff format --check src/ tests/` | ✅ |
| Type check | `mypy src/ --ignore-missing-imports` | ✅ |
| Tests | `pytest tests/ -v --cov=src` | ✅ |
| Security | `pip-audit --desc` | ⚠️ warn-only |
| Best practices | AST type hint check | ✅ |

---

## Branch Structure

```
main (prod) ← 2 approvals
  └── uat ← 1 approval
        └── sit ← 1 approval
              └── qa ← 1 approval
                    └── dev ← 1 approval
                          ├── feat/*
                          ├── hotfix/*
                          └── bugfix/*
```

---

## Cron Jobs

| Job ID | Name | Schedule |
|--------|------|----------|
| `e1deadafefd4` | project-health-monitor | every 30m |
| `7eb8fde941a9` | spec-intake-monitor | every 10m |

---

## How to Continue

### New Feature
```bash
git checkout dev && git pull
git checkout -b feat/my-feature
cp .hermes/specs/TEMPLATE.md .hermes/specs/my-feature.md
"process specs"
```

### Bug Fix
```bash
cp .hermes/specs/TEMPLATE.md .hermes/specs/bug-fix.md
"fix this bug"
```

### Refactor
```bash
"refactor module X"
```

---

## Key Files to Read

1. `.hermes.md` — Project rules (agent auto-load)
2. `.hermes/best-practices.md` — Coding standards
3. `docs/INDEX.md` — Documentation map
4. `docs/API.md` — API reference
5. `docs/WORKFLOW.md` — Flow + branching

---

## Key Commands

```bash
# Validation (full pipeline)
python scripts/pre_commit_validate.py

# Tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Format code
ruff format src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/ --ignore-missing-imports

# Health check
python scripts/check_project_health.py

# GitHub
"/c/Program Files/GitHub CLI/gh.exe" pr list
"/c/Program Files/GitHub CLI/gh.exe" run list
```

---

*Last updated: 2026-08-27*