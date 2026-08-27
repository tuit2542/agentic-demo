# Agentic Full-Loop Engineering — User Guide

> คู่มือการใช้งาน Agentic Development Workflow สำหรับ Hermes Agent

---

## ภาพรวม

```
┌──────────────────────────────────────────────────────────────────────┐
│                     AGENTIC FULL LOOP (Complete)                      │
│                                                                       │
│  Spec → Best Practices → Plan → TDD → Validate → Commit → GitHub     │
│    │         │              │       │           │          │          │
│    │         │              │       │           │          │          │
│    ▼         ▼              ▼       ▼           ▼          ▼          │
│  .hermes/  .hermes/      .hermes/  ruff      git        gh CLI      │
│  specs/    best-         plans/    mypy      commit     push        │
│            practices.md            pytest               PR/CI       │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │  MISSING: CI/CD + Branch Protection + Code Review + Coverage│     │
│  └─────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## โครงสร้างไฟล์

```
project-root/
├── .hermes.md                    ← Project rules (agent auto-load)
├── AGENTS.md                     ← Portable agent rules
├── CHANGELOG.md                  ← Version history (Keep-a-Changelog)
├── GITHUB_INTEGRATION.md         ← GitHub setup guide
├── AGENTIC_WORKFLOW.md           ← ไฟล์นี้
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
│   └── ci.yml                    ← ❌ ยังไม่มี (ต้องสร้าง)
├── src/
├── tests/
└── requirements.txt
```

---

## Current Flow Status

### ✅ ทำแล้ว (100% Local)

| Step | Status | Detail |
|------|--------|--------|
| Spec intake | ✅ | `.hermes/specs/` + `read_specs.py` + cron |
| Best practices | ✅ | `.hermes/best-practices.md` (auto-load) |
| Plan generation | ✅ | `.hermes/plans/` + `spec-intake` skill |
| TDD workflow | ✅ | `agentic-full-loop` skill |
| Pre-commit validation | ✅ | 4 checks: lint + type + test + security |
| Git commit | ✅ | Conventional commits + auto-validate |
| GitHub push | ✅ | `gh` CLI authenticated as tuit2542 |
| Health monitoring | ✅ | Cron job ทุก 30 นาที (continuity) |

### ❌ ยังไม่มี (ต้องสร้าง)

| Step | Status | สำคัญแค่ไหน | วิธีทำ |
|------|--------|------------|--------|
| CI/CD pipeline | ❌ | 🔴 สูง | GitHub Actions workflow |
| Branch protection | ❌ | 🔴 สูง | GitHub settings |
| PR creation automation | ❌ | 🟡 กลาง | Agent สร้าง PR อัตโนมัติ |
| Code review automation | ❌ | 🟡 กลาง | `requesting-code-review` skill |
| Test coverage | ❌ | 🟡 กลาง | pytest-cov + coverage report |
| Dependency auto-update | ❌ | 🟢 ต่ำ | Dependabot/Renovate |

---

## Flow ที่ต้องการ (Target State)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    TARGET: COMPLETE FULL LOOP                         │
│                                                                       │
│  Spec → Best Practices → Plan → TDD → Validate → Commit → PR → CI   │
│    │         │              │       │           │       │      │      │
│    │         │              │       │           │       │      │      │
│    ▼         ▼              ▼       ▼           ▼       ▼      ▼      │
│  .hermes/  .hermes/      .hermes/  4 checks   git    gh     Actions │
│  specs/    best-         plans/              commit  PR     validate │
│            practices.md                                         merge  │
│                                                                       │
│  Missing pieces:                                                      │
│  ├── .github/workflows/ci.yml                                        │
│  ├── Branch protection rules                                         │
│  └── Auto PR creation skill                                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## วิธีใช้งาน

### 1. เริ่มต้นใช้งานครั้งแรก

```bash
# Clone หรือ copy .hermes/ folder ไป project ใหม่
cp -r .hermes/ /path/to/new-project/
cp .hermes.md /path/to/new-project/
cp AGENTS.md /path/to/new-project/
cp scripts/ /path/to/new-project/scripts/

# แก้ validation.json ตาม stack ที่ใช้
# แก้ .hermes.md ตาม project requirements
```

### 2. แปะ Spec File

```bash
cp .hermes/specs/TEMPLATE.md .hermes/specs/my-feature.md
# แก้ไข my-feature.md ตามต้องการ
```

### 3. ให้ Agent Process

```bash
"process specs"
```

Agent จะ:
1. อ่าน `best-practices.md`
2. อ่าน spec files ทุกตัว
3. สร้าง implementation plan
4. ลุย TDD workflow
5. Validate → Commit

### 4. ตรวจสอบสถานะ

```bash
# Health monitor (cron รันทุก 30 นาที)
python scripts/check_project_health.py
```

---

## Language Support

| Language | Detect Pattern | Commands |
|----------|---------------|----------|
| Python | `*.py`, `requirements.txt` | ruff, mypy, pytest, pip-audit |
| JavaScript | `*.js`, `package.json` | eslint, tsc, npm test, npm audit |
| TypeScript | `*.ts`, `tsconfig.json` | eslint, tsc, npm test, npm audit |
| Rust | `Cargo.toml` | clippy, cargo check, cargo test, cargo audit |
| Go | `go.mod` | golangci-lint, go vet, go test, govulncheck |

---

## Best Practices Rules

### Core Principles (ทุก language)

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

## Cron Jobs

| Job ID | Name | Schedule | Feature |
|--------|------|----------|---------|
| `e1deadafefd4` | project-health-monitor | every 30m | continuity |
| `7eb8fde941a9` | spec-intake-monitor | every 10m | continuity |

---

## Skills

| Skill | หน้าที่ | ใช้เมื่อไหร่ |
|-------|--------|-------------|
| `agentic-full-loop` | TDD workflow | implement feature |
| `spec-intake` | Read spec → plan | process specs |
| `plan` | สร้าง plan | เริ่ม task ใหม่ |
| `test-driven-development` | RED→GREEN→REFACTOR | เขียน code |
| `requesting-code-review` | Independent review | ก่อน commit |
| `systematic-debugging` | Root cause analysis | bug แก้ไม่หาย |
| `github-pr-workflow` | PR lifecycle | push ขึ้น GitHub |

---

## Workflow Templates

### Template 1: Feature Development

```
1. แปะ spec: .hermes/specs/feature-name.md
2. บอก agent: "process specs"
3. Agent สร้าง plan
4. Agent ลุย TDD
5. Pre-commit hook validate
6. Commit + push
7. ❌ สร้าง PR (ยังไม่มี)
8. ❌ CI validate (ยังไม่มี)
```

### Template 2: Bug Fix

```
1. แปะ bug report: .hermes/specs/bug-fix.md
2. บอก agent: "fix this bug"
3. Agent ใช้ systematic-debugging skill
4. Agent สร้าง regression test
5. Agent แก้ bug
6. Validate → Commit → Push
```

### Template 3: Refactor

```
1. บอก agent: "refactor module X"
2. Agent ใช้ simplify-code skill
3. Agent สร้าง plan
4. Agent refactor ทีละจุด (tests pass ตลอด)
5. Validate → Commit → Push
```

### Template 4: Code Review

```
1. บอก agent: "review recent changes"
2. Agent ใช้ requesting-code-review skill
3. Agent report findings
4. Agent แก้ไขถ้ามี issues
5. Validate → Commit → Push
```

---

## Quick Reference

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
"/c/Program Files/GitHub CLI/gh.exe" repo list
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

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Spec not detected | Check file is in `.hermes/specs/` and not `done/` |
| Validation fails | Run `python scripts/pre_commit_validate.py` |
| Cron not firing | Check `hermes gateway status` |
| Script not found | Copy script to `~/.hermes/scripts/` |
| Language not detected | Add detect patterns in `validation.json` |
| gh not found | Use full path: `/c/Program Files/GitHub CLI/gh.exe` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.2.0 | 2026-08-26 | FastAPI migration + full validation pipeline |
| v0.1.0 | 2026-08-26 | Initial Flask implementation |

---

*Last updated: 2026-08-27*
