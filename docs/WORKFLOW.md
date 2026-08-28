# Workflow & Branching

> Agentic Demo — Development workflow

---

## Flow Diagram

```
Spec → Best Practices → Plan → TDD → Validate → Commit → PR → CI → Review → Merge → Auto-Promote → Auto-Deploy
         ↑                                                                        ↓
         └────────────────────────────────────────────────────────────────────────┘
```

---

## Feature Development

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

---

## Bug Fix

```
1. แปะ bug report: .hermes/specs/bug-fix.md
2. บอก agent: "fix this bug"
3. Agent ใช้ systematic-debugging skill
4. Agent สร้าง regression test
5. Agent แก้ bug
6. Validate → Commit → Push
7. Agent สร้าง PR
```

---

## Refactor

```
1. บอก agent: "refactor module X"
2. Agent ใช้ simplify-code skill
3. Agent สร้าง plan
4. Agent refactor ทีละจุด (tests pass ตลอด)
5. Validate → Commit → Push
6. Agent สร้าง PR
```

---

## Branching Strategy

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

## Doc Updates

| Doc Change | Branch | Flow |
|------------|--------|------|
| Small (typo, 1-2 lines) | dev | PR to dev |
| Large (restructure) | feat/doc-* | PR to dev |
| Emergency (prod data) | hotfix/doc-* | PR to main + backport |

---

*Last updated: 2026-08-27*