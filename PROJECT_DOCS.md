# PROJECT DOCS

> รวม文档ทั้งหมดของ Agentic Demo — ไฟล์เดียวจบ

---

## 1. Overview

**ชื่อ:** Agentic Demo — URL Shortener
**Stack:** Python 3.11, FastAPI, Pydantic v2, pytest, ruff, mypy
**Repo:** https://github.com/tuit2542/agentic-demo
**Status:** v0.2.0 — MVP พร้อมใช้งาน

---

## 2. Project Structure

```
agentic-demo/
├── .hermes.md                    ← Project rules (agent auto-load)
├── AGENTS.md                     ← Portable agent rules
├── PROJECT_DOCS.md               ← ไฟล์นี้
├── .hermes/
│   ├── best-practices.md         ← Central best practices registry
│   ├── validation.json           ← Language-agnostic validation config
│   ├── specs/                    ← Feature specs (user แปะที่นี่)
│   │   ├── TEMPLATE.md           ← Spec template
│   │   └── done/                 ← Processed specs
│   └── plans/                    ← Implementation plans (agent สร้าง)
├── scripts/
│   ├── pre_commit_validate.py    ← Auto-validation pipeline (4 checks)
│   ├── read_specs.py             ← Spec reader → plan generator
│   └── check_project_health.py   ← Cron health monitor
├── .github/workflows/
│   ├── ci.yml                    ← GitHub Actions CI pipeline
│   ├── auto-promote.yml          ← Auto-create PR to next env
│   └── deploy.yml                ← Auto-deploy to environment
├── src/
│   ├── __init__.py
│   ├── app.py                    ← FastAPI application
│   ├── models.py                 ← Pydantic models
│   └── store.py                  ← In-memory storage
├── tests/
│   ├── test_app.py               ← API tests
│   ├── test_models.py            ← Model tests
│   └── test_store.py             ← Store tests
└── requirements.txt
```

---

## 3. API Reference

### Endpoints

| Endpoint | Method | Request Body | Response | ใช้ทำอะไร |
|----------|--------|--------------|----------|----------|
| `/` | GET | - | `{"message": "URL Shortener API"}` | Health check |
| `/shorten` | POST | `{"url": "https://example.com"}` | `{"short_id": "abc123", "original_url": "..."}` | สร้าง short URL |
| `/{short_id}` | GET | - | 307 Redirect | Redirect ไป original URL |
| `/{short_id}/stats` | GET | - | `{"short_id": "abc123", "original_url": "...", "clicks": 5}` | ดูสถิติ |

### Models

| Model | Fields | ใช้ทำอะไร |
|-------|--------|----------|
| `ShortenRequest` | `url: str` (validated) | Validate input ตอนสร้าง short URL |
| `ShortenResponse` | `short_id: str`, `original_url: str`, `created_at: str` | Response ตอนสร้าง short URL |
| `StatsResponse` | `short_id: str`, `original_url: str`, `clicks: int` | Response ตอนดูสถิติ |

### Store

| Class | Methods | ใช้ทำอะไร |
|-------|---------|----------|
| `UrlStore` | `shorten(url) -> short_id` | สร้าง short ID จาก URL |
| `UrlStore` | `resolve(short_id) -> url` | หา original URL จาก short ID |
| `UrlStore` | `stats(short_id) -> dict` | ดูข้อมูล + click count |

**Logic:**
- Short ID: 6-char alphanumeric (a-z, A-Z, 0-9)
- Storage: Python dict (in-memory, ไม่ persist)
- Click count: เพิ่มทุกครั้งที่ resolve

### Tests

| File | Tests | Status |
|------|-------|--------|
| `tests/test_store.py` | 5 tests | ✅ |
| `tests/test_models.py` | 5 tests | ✅ |
| `tests/test_app.py` | 6 tests | ✅ |
| **Total** | **16 tests** | **✅ All pass** |

---

## 4. Workflow

### Flow Diagram

```
Spec → Best Practices → Plan → TDD → Validate → Commit → PR → CI → Review → Merge → Auto-Promote → Auto-Deploy
         ↑                                                                        ↓
         └────────────────────────────────────────────────────────────────────────┘
```

### Auto-Update Flow

```
Agent ทำงานเสร็จ → auto-update PROJECT_DOCS.md
├── เพิ่ม API ใหม่ → update API Reference
├── เพิ่ม feature → update Changelog
├── เปลี่ยน workflow → update Workflow
└── update Context Handoff (ทุกครั้ง)
```

### Feature Development

```
1. แปะ spec: .hermes/specs/feature-name.md
2. บอก agent: "process specs"
3. Agent สร้าง plan
4. Agent ลุย TDD
5. Pre-commit hook validate
6. Commit + push
7. Agent สร้าง PR
8. CI ทำงาน → Review → Merge
9. Auto-promote: dev → qa → sit → uat → main
10. Auto-deploy ทำงานอัตโนมัติ
```

### Bug Fix

```
1. แปะ bug report: .hermes/specs/bug-fix.md
2. บอก agent: "fix this bug"
3. Agent ใช้ systematic-debugging skill
4. Agent สร้าง regression test
5. Agent แก้ bug
6. Validate → Commit → Push
7. Agent สร้าง PR
```

### Refactor

```
1. บอก agent: "refactor module X"
2. Agent ใช้ simplify-code skill
3. Agent สร้าง plan
4. Agent refactor ทีละจุด (tests pass ตลอด)
5. Validate → Commit → Push
6. Agent สร้าง PR
```

---

## 5. Branching Strategy

### Branch Structure

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

### Branch Roles

| Branch | Purpose | Deploy To | Protected |
|--------|---------|-----------|-----------|
| `main` | Production code | Production | ✅ 2 approvals |
| `uat` | User acceptance testing | UAT environment | ✅ 1 approval |
| `sit` | System integration testing | SIT environment | ✅ 1 approval |
| `qa` | Quality assurance testing | QA environment | ✅ 1 approval |
| `dev` | Development integration | Dev environment | ✅ 1 approval |
| `feat/*` | New features | None | ❌ |
| `hotfix/*` | Emergency fixes | None | ❌ |
| `bugfix/*` | Bug fixes | None | ❌ |

### Merge Flow

```
feat/* ──→ dev ──→ qa ──→ sit ──→ uat ──→ main
           │       │       │       │       │
           ▼       ▼       ▼       ▼       ▼
        CI Pass  CI Pass CI Pass CI Pass CI Pass
        1 Rev    1 Rev   1 Rev   2 Rev   2 Rev
```

---

## 6. Validation Pipeline

### Checks

| Check | Command | Must Pass |
|-------|---------|-----------|
| Lint | `python -m ruff check src/ tests/` | ✅ |
| Type check | `python -m mypy src/ --ignore-missing-imports` | ✅ |
| Tests | `python -m pytest tests/ -v` | ✅ |
| Security | `python -m pip-audit --desc` | ⚠️ warn-only |

### Language Support

| Language | Detect Pattern | Commands |
|----------|---------------|----------|
| Python | `*.py`, `requirements.txt` | ruff, mypy, pytest, pip-audit |
| JavaScript | `*.js`, `package.json` | eslint, tsc, npm test, npm audit |
| TypeScript | `*.ts`, `tsconfig.json` | eslint, tsc, npm test, npm audit |
| Rust | `Cargo.toml` | clippy, cargo check, cargo test, cargo audit |
| Go | `go.mod` | golangci-lint, go vet, go test, govulncheck |

---

## 7. Best Practices

### Core Principles

1. **TDD is non-negotiable** — test first, then implement
2. **Type safety** — type hints on all public functions
3. **Validate before commit** — lint + type check + test + security
4. **Small focused changes** — one feature per commit
5. **Defensive coding** — handle errors explicitly

### Quality Gates

| Gate | When | Must Pass |
|------|------|-----------|
| Lint | Before commit | ✅ |
| Type check | Before commit | ✅ |
| Tests | Before commit | ✅ |
| Security | Before commit | ⚠️ warn-only |

---

## 8. Cron Jobs

| Job ID | Name | Schedule | Feature |
|--------|------|----------|---------|
| `e1deadafefd4` | project-health-monitor | every 30m | continuity |
| `7eb8fde941a9` | spec-intake-monitor | every 10m | continuity |

---

## 9. Skills

| Skill | หน้าที่ | ใช้เมื่อไหร่ |
|-------|--------|-------------|
| `agentic-full-loop` | TDD workflow | implement feature |
| `spec-intake` | Read spec → plan | process specs |
| `plan` | สร้าง plan | เริ่ม task ใหม่ |
| `test-driven-development` | RED→GREEN→REFACTOR | เขียน code |
| `requesting-code-review` | Independent review | ก่อน commit |
| `systematic-debugging` | Root cause analysis | bug แก้ไม่หาย |
| `github-pr-workflow` | PR lifecycle | push ขึ้น GitHub |
| `github-pr-create` | Create PR | หลังจาก commit และ push |

---

## 10. Context Handoff

### สำหรับ AI ที่จะทำงานต่อ

1. **อ่านไฟล์นี้ก่อน** — เพื่อรู้ว่าทำอะไรไปแล้วบ้าง
2. **อ่าน `.hermes/best-practices.md`** — เพื่อรู้ coding standards
3. **ดู git log** — เพื่อรู้ว่า commit ล่าสุดคืออะไร

### สำหรับ User

- แปะ spec ไฟล์ใน `.hermes/specs/` แล้วบอก agent ว่า "process specs"
- Agent จะสร้าง plan → TDD → validate → commit → PR อัตโนมัติ
- Auto-promote จะทำงานเมื่อ merge แต่ละ branch

---

## 11. Changelog

### [Unreleased]
- Best practices registry
- Spec intake pipeline with auto-detect
- Pre-commit validation pipeline (language-agnostic)
- Project health monitor cron job with continuity
- Agentic workflow user guide
- Enterprise branching strategy
- Auto-promote workflow
- Deploy workflow
- PR creation skill
- API tracking
- Context handoff

### [0.2.0] - 2026-08-26
- Pydantic v2 models with type validation
- FastAPI async endpoints
- Async test client with httpx
- mypy type checking in validation pipeline

### [0.1.0] - 2026-08-26
- Initial Flask URL shortener implementation
- In-memory URL store with click tracking
- Basic test suite (pytest)
- Linting with ruff
- Git repository setup with conventional commits

---

## 12. Quick Reference

### Commands

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
"/c/Program Files/GitHub CLI/gh.exe" run list
```

### Agent Instructions

```bash
# Process specs
"process specs"

# Implement feature
"implement [feature name] using TDD"

# Fix bug
"fix [bug description]"

# Review code
"review recent changes"

# Refactor
"refactor [module name]"

# Create PR
"create PR for recent changes"
```

---

## 13. Troubleshooting

| Problem | Solution |
|---------|----------|
| Spec not detected | Check file is in `.hermes/specs/` and not `done/` |
| Validation fails | Run `python scripts/pre_commit_validate.py` |
| Cron not firing | Check `hermes gateway status` |
| Script not found | Copy script to `~/.hermes/scripts/` |
| Language not detected | Add detect patterns in `validation.json` |
| gh not found | Use full path: `/c/Program Files/GitHub CLI/gh.exe` |
| PR creation failed | ตรวจสอบว่ามีการ commit ใหม่หรือไม่ |

---

## 14. Future Features

| Feature | Priority | สถานะ |
|---------|----------|--------|
| SQLite/PostgreSQL storage | 🔴 สูง | ❌ ยังไม่มี |
| Rate limiting | 🔴 สูง | ❌ ยังไม่มี |
| JWT authentication | 🟡 กลาง | ❌ ยังไม่มี |
| Custom short ID | 🟡 กลาง | ❌ ยังไม่มี |
| URL expiration | 🟡 กลาง | ❌ ยังไม่มี |
| Click analytics | 🟢 ต่ำ | ❌ ยังไม่มี |

---

*Last updated: 2026-08-27*
