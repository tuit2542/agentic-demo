# Context Handoff

> ไฟล์นี้สำหรับส่งมอบ context ไปยัง AI session ใหม่ เมื่อ context window เต็ม

---

## Current State (2026-08-27)

### สถานะโปรเจค

```
Repo: https://github.com/tuit2542/agentic-demo
Branch: main (protected)
Last commit: 8a13b39 (Merge pull request #3 - auto-promote + deploy workflows)
Tags: v0.1.0, v0.2.0
```

### สิ่งที่ทำเสร็จแล้ว

| # | Feature | Status | ไฟล์ |
|---|---------|--------|------|
| 1 | URL Shortener API (FastAPI) | ✅ | `src/app.py` |
| 2 | Pydantic models | ✅ | `src/models.py` |
| 3 | In-memory store | ✅ | `src/store.py` |
| 4 | 16 tests (all pass) | ✅ | `tests/` |
| 5 | Pre-commit validation (4 checks) | ✅ | `scripts/pre_commit_validate.py` |
| 6 | Language-agnostic validation | ✅ | `.hermes/validation.json` |
| 7 | Spec intake pipeline | ✅ | `scripts/read_specs.py` |
| 8 | Health monitor cron | ✅ | `scripts/check_project_health.py` |
| 9 | GitHub Actions CI | ✅ | `.github/workflows/ci.yml` |
| 10 | Auto-promote workflow | ✅ | `.github/workflows/auto-promote.yml` |
| 11 | Deploy workflow | ✅ | `.github/workflows/deploy.yml` |
| 12 | Branch protection (5 branches) | ✅ | GitHub settings |
| 13 | Enterprise branching strategy | ✅ | `BRANCHING_STRATEGY.md` |
| 14 | PR creation skill | ✅ | `skills/github-pr-create` |
| 15 | Agentic workflow documentation | ✅ | `AGENTIC_WORKFLOW.md` |
| 16 | API tracking | ✅ | `API_TRACKING.md` |
| 17 | Best practices registry | ✅ | `.hermes/best-practices.md` |
| 18 | SOUL.md (global) | ✅ | `~/.hermes/SOUL.md` |

### สิ่งที่ยังไม่ได้ทำ

| # | Feature | Priority | หมายเหตุ |
|---|---------|----------|---------|
| 1 | SQLite/PostgreSQL storage | 🔴 สูง | ตอนนี้ใช้ in-memory dict |
| 2 | Rate limiting | 🔴 สูง | ป้องกัน abuse |
| 3 | JWT authentication | 🟡 กลาง | สำหรับ protected endpoints |
| 4 | Custom short ID | 🟡 กลาง | ให้ user กำหนดเอง |
| 5 | URL expiration | 🟡 กลาง | auto-delete หลังหมดอายุ |
| 6 | Click analytics | 🟢 ต่ำ | รายละเอียดการเข้าถึง |

---

## Branch Structure

```
main (prod) ← 2 approvals required
  └── uat ← 1 approval required
        └── sit ← 1 approval required
              └── qa ← 1 approval required
                    └── dev ← 1 approval required
                          ├── feat/*
                          ├── hotfix/*
                          └── bugfix/*
```

## Cron Jobs

| Job ID | Name | Schedule | Feature |
|--------|------|----------|---------|
| `e1deadafefd4` | project-health-monitor | every 30m | continuity |
| `7eb8fde941a9` | spec-intake-monitor | every 10m | continuity |

---

## How to Continue

### ถ้าจะเริ่ม Feature ใหม่

```bash
# 1. Sync dev
git checkout dev && git pull

# 2. สร้าง feature branch
git checkout -b feat/my-feature

# 3. แปะ spec
cp .hermes/specs/TEMPLATE.md .hermes/specs/my-feature.md

# 4. บอก agent
"process specs"

# 5. Agent ลุย TDD → validate → commit → push → PR
```

### ถ้าจะแก้ Bug

```bash
# 1. แปะ bug report
cp .hermes/specs/TEMPLATE.md .hermes/specs/bug-fix.md

# 2. บอก agent
"fix this bug"

# 3. Agent ใช้ systematic-debugging skill
```

### ถ้าจะ Refactor

```bash
# 1. บอก agent
"refactor module X"

# 2. Agent ใช้ simplify-code skill
```

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

# Lint
ruff check src/ tests/

# Type check
mypy src/ --ignore-missing-imports

# GitHub
"/c/Program Files/GitHub CLI/gh.exe" pr list
"/c/Program Files/GitHub CLI/gh.exe" api repos/tuit2542/agentic-demo/actions/runs --jq '.workflow_runs[0:3] | .[] | "\(.head_sha[0:7]) \(.name) \(.status) \(.conclusion)"'
```

---

## AI Session Instructions

### สำหรับ AI ที่จะทำงานต่อ

1. **อ่านไฟล์นี้ก่อน** — เพื่อรู้ว่าทำอะไรไปแล้วบ้าง
2. **อ่าน `AGENTIC_WORKFLOW.md`** — เพื่อรู้ workflow ทั้งหมด
3. **อ่าน `BRANCHING_STRATEGY.md`** — เพื่อรู้ branching pattern
4. **อ่าน `.hermes/best-practices.md`** — เพื่อรู้ coding standards
5. **อ่าน `API_TRACKING.md`** — เพื่อรู้ว่ามี API อะไรบ้าง

### สำหรับ User

- แปะ spec ไฟล์ใน `.hermes/specs/` แล้วบอก agent ว่า "process specs"
- Agent จะสร้าง plan → TDD → validate → commit → PR อัตโนมัติ
- Auto-promote จะทำงานเมื่อ merge แต่ละ branch

---

*Last updated: 2026-08-27*
