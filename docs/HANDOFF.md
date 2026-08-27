# Context Handoff

> สำหรับ AI session ใหม่ — อ่านไฟล์นี้ก่อนเริ่มงาน

---

## Current State (2026-08-27)

### Project
- **Repo:** https://github.com/tuit2542/agentic-demo
- **Branch:** main (protected, 2 approvals)
- **Last commit:** docs split into docs/ folder
- **Tags:** v0.1.0, v0.2.0

### What's Done

| # | Feature | Status |
|---|---------|--------|
| 1 | URL Shortener API (FastAPI) | ✅ |
| 2 | Pydantic models | ✅ |
| 3 | In-memory store | ✅ |
| 4 | 16 tests passing | ✅ |
| 5 | Pre-commit validation (4 checks) | ✅ |
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
# Validation
python scripts/pre_commit_validate.py

# Spec reader
python scripts/read_specs.py

# Health check
python scripts/check_project_health.py

# Tests
pytest tests/ -v

# GitHub
"/c/Program Files/GitHub CLI/gh.exe" pr list
"/c/Program Files/GitHub CLI/gh.exe" run list
```

---

*Last updated: 2026-08-27*