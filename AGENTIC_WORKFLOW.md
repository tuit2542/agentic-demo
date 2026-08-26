# Agentic Full-Loop Engineering — User Guide

> คู่มือการใช้งาน Agentic Development Workflow สำหรับ Hermes Agent

---

## ภาพรวม

ระบบ Agentic Development ที่ครบวงจร — ตั้งแต่รับ requirement จนถึง ship code

```
┌─────────────────────────────────────────────────────────┐
│                  AGENTIC FULL LOOP                       │
│                                                          │
│  Spec → Best Practices → Plan → TDD → Validate → Commit  │
│    │         │              │       │           │         │
│    │         │              │       │           │         │
│    ▼         ▼              ▼       ▼           ▼         │
│  .hermes/  .hermes/      .hermes/  ruff      git         │
│  specs/    best-         plans/    mypy      commit      │
│            practices.md            pytest                 │
└─────────────────────────────────────────────────────────┘
```

---

## โครงสร้างไฟล์

```
project-root/
├── .hermes.md                    ← Project rules (agent auto-load)
├── AGENTS.md                     ← Portable agent rules
├── SOUL.md                       ← Agent identity (global, อยู่ที่ ~/.hermes/)
├── .hermes/
│   ├── best-practices.md         ← Central best practices registry
│   ├── validation.json           ← Language-agnostic validation config
│   ├── specs/                    ← Feature specs (user แปะที่นี่)
│   │   ├── TEMPLATE.md           ← Spec template
│   │   └── done/                 ← Processed specs
│   └── plans/                    ← Implementation plans (agent สร้าง)
├── scripts/
│   ├── pre_commit_validate.py    ← Auto-validation pipeline
│   ├── read_specs.py             ← Spec reader → plan generator
│   └── check_project_health.py   ← Cron health monitor
├── src/
├── tests/
└── requirements.txt
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
# Copy template
cp .hermes/specs/TEMPLATE.md .hermes/specs/my-feature.md

# แก้ไข my-feature.md ตามต้องการ
```

**ตัวอย่าง spec:**
```markdown
# Feature: JWT Authentication

## User Story
As a developer, I want JWT auth so that API endpoints are secured.

## Requirements
- [ ] Login endpoint returns JWT token
- [ ] Middleware validates token on protected routes
- [ ] Token expires after 24 hours

## Acceptance Criteria
- [ ] Given valid credentials, when login, then token returned
- [ ] Given valid token, when access protected route, then 200 OK
- [ ] Given expired token, when access protected route, then 401 Unauthorized
```

### 3. ให้ Agent Process

```bash
# บอก agent
"process specs"

# หรือ agent จะ auto-detect ผ่าน cron
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
# ดู output ล่าสุด
cat D:\Users\pongsathornb\AppData\Local\hermes\cron\output\e1deadafefd4\*.md

# หรือรัน manual
python scripts/check_project_health.py
```

---

## Language Support

### Auto-Detect

`validation.json` auto-detect language จากไฟล์ใน project:

| Language | Detect Pattern | Commands |
|----------|---------------|----------|
| Python | `*.py`, `requirements.txt` | ruff, mypy, pytest |
| JavaScript | `*.js`, `package.json` | eslint, tsc, npm test |
| TypeScript | `*.ts`, `tsconfig.json` | eslint, tsc, npm test |
| Rust | `Cargo.toml` | clippy, cargo check, cargo test |
| Go | `go.mod` | golangci-lint, go vet, go test |

### เปลี่ยน Stack

แก้ `.hermes/validation.json`:

```json
{
  "language_configs": {
    "python": {
      "detect": ["*.py"],
      "lint": "python -m ruff check src/",
      "type_check": "python -m mypy src/",
      "test": "python -m pytest tests/ -v"
    }
  }
}
```

---

## Best Practices Rules

### Auto-Load Flow

```
Agent start
    ↓
Read .hermes.md
    ↓
Read .hermes/best-practices.md
    ↓
Load language-specific rules
    ↓
Start task
```

### Core Principles (ทุก language)

1. **TDD is non-negotiable** — test first, then implement
2. **Type safety** — type hints on all public functions
3. **Validate before commit** — lint + type check + test
4. **Small focused changes** — one feature per commit
5. **Defensive coding** — handle errors explicitly

### Quality Gates

| Gate | When | Must Pass |
|------|------|-----------|
| Lint | Before commit | ✅ |
| Type check | Before commit | ✅ |
| Tests | Before commit | ✅ |

---

## Cron Jobs

### Active Jobs

| Job ID | Name | Schedule | Feature |
|--------|------|----------|---------|
| `e1deadafefd4` | project-health-monitor | every 30m | continuity |

### Continuity

Cron job จำ output เก่าไว้ เปรียบเทียบกับ run ถัดไป:
- Run 1: `{"src_files": 4}`
- Run 2: `{"src_files": 5}` → agent เห็นว่าเพิ่มมา 1 file

---

## Skills

### ตัวที่สร้างแล้ว

| Skill | หน้าที่ | ใช้เมื่อไหร่ |
|-------|--------|-------------|
| `agentic-full-loop` | TDD workflow | implement feature |
| `spec-intake` | Read spec → plan | process specs |
| `plan` | สร้าง plan | เริ่ม task ใหม่ |
| `test-driven-development` | RED→GREEN→REFACTOR | เขียน code |
| `requesting-code-review` | Independent review | ก่อน commit |
| `systematic-debugging` | Root cause analysis | bug แก้ไม่หาย |
| `github-pr-workflow` | PR lifecycle | push ขึ้น GitHub |

### วิธีใช้ Skill

```python
# Auto-detect (agent scan skills แล้วเลือกเอง)
"implement auth feature"

# Manual load
skill_view(name="agentic-full-loop")

# ใน delegate_task
delegate_task(
    goal="Implement auth module",
    context="Follow agentic-full-loop skill"
)
```

---

## ข้อแนะนำเพิ่มเติม (Recommendations)

### 🔴 Priority สูง — ควรทำเร็วๆ นี้

| # | สิ่งที่ควรทำ | ทำไม | วิธีทำ |
|---|------------|------|--------|
| 1 | **ตั้ง GitHub auth** | push ขึ้น remote ได้ | ใช้ `github-auth` skill |
| 2 | **เพิ่ม CHANGELOG.md** | track version history | สร้างไฟล์ + ปรับ git hook |
| 3 | **ตั้ง cron spec-intake** | auto-process specs ทุก 10 นาที | `cronjob(action="create")` |
| 4 | **เพิ่ม security scan** | scan vulnerabilities ก่อน release | เพิ่ม command ใน validation.json |

### 🟡 Priority กลาง — ควรทำเร็วๆ นี้

| # | สิ่งที่ควรทำ | ทำไม | วิธีทำ |
|---|------------|------|--------|
| 5 | **เพิ่ม ADR** | record architecture decisions | สร้าง `.hermes/adr/` |
| 6 | **ตั้ง branch protection** | ป้องกัน push ตรง main | GitHub settings |
| 7 | **เพิ่ม CI/CD** | auto-validate บน cloud | GitHub Actions workflow |
| 8 | **Monitor performance** | track test coverage | เพิ่ม coverage report |

### 🟢 Priority ต่ำ — ทำเมื่อมีเวลา

| # | สิ่งที่ควรทำ | ทำไม | วิธีทำ |
|---|------------|------|--------|
| 9 | **Multi-agent orchestration** | parallel development | delegate_task + agent teams |
| 10 | **Documentation site** | share knowledge | MkDocs หรือ Docusaurus |
| 11 | **Dependency scanning** | auto-update deps | Dependabot หรือ Renovate |
| 12 | **Performance profiling** | optimize bottlenecks | cProfile, py-spy |

---

## Workflow Templates

### Template 1: Feature Development

```
1. แปะ spec: .hermes/specs/feature-name.md
2. บอก agent: "process specs"
3. Agent สร้าง plan
4. Agent ลุย TDD
5. Pre-commit hook validate
6. Commit + tag
```

### Template 2: Bug Fix

```
1. แปะ bug report: .hermes/specs/bug-fix.md
2. บอก agent: "fix this bug"
3. Agent ใช้ systematic-debugging skill
4. Agent สร้าง regression test
5. Agent แก้ bug
6. Validate → Commit
```

### Template 3: Refactor

```
1. บอก agent: "refactor module X"
2. Agent ใช้ simplify-code skill
3. Agent สร้าง plan
4. Agent refactor ทีละจุด ( tests pass ตลอด)
5. Validate → Commit
```

### Template 4: Code Review

```
1. บอก agent: "review recent changes"
2. Agent ใช้ requesting-code-review skill
3. Agent report findings
4. Agent แก้ไขถ้ามี issues
5. Validate → Commit
```

---

## Quick Reference

### Commands ที่ใช้บ่อย

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
```

### Cron Management

```bash
# List jobs
cronjob(action="list")

# Run manual
cronjob(action="run", job_id="e1deadafefd4")

# Pause
cronjob(action="pause", job_id="e1deadafefd4")

# Resume
cronjob(action="resume", job_id="e1deadafefd4")
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Spec not detected | Check file is in `.hermes/specs/` and not `done/` |
| Validation fails | Run `python scripts/pre_commit_validate.py` to see which step fails |
| Cron not firing | Check `hermes gateway status` |
| Script not found | Copy script to `~/.hermes/scripts/` |
| Language not detected | Add detect patterns in `validation.json` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.2.0 | 2026-08-26 | FastAPI migration + full validation pipeline |
| v0.1.0 | 2026-08-26 | Initial Flask implementation |

---

*Last updated: 2026-08-26*
