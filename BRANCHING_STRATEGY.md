# Enterprise Branching Strategy

> Git Flow สำหรับ Agentic Development — แยก environment ชัดเจน

---

## Branch Structure

```
main (prod)
  └── uat (User Acceptance Testing)
        └── sit (System Integration Testing)
              └── qa (Quality Assurance)
                    └── dev (Development)
                          ├── feat/* (Feature branches)
                          ├── hotfix/* (Emergency fixes)
                          └── bugfix/* (Bug fixes)
```

## Branch Roles

| Branch | Purpose | Deploy To | Protected |
|--------|---------|-----------|-----------|
| `main` | Production code | Production | ✅ Require PR + CI + 2 approvals |
| `uat` | User acceptance testing | UAT environment | ✅ Require PR + CI + 1 approval |
| `sit` | System integration testing | SIT environment | ✅ Require PR + CI |
| `qa` | Quality assurance testing | QA environment | ✅ Require PR + CI |
| `dev` | Development integration | Dev environment | ✅ Require PR + CI |
| `feat/*` | New features | None (local only) | ❌ |
| `hotfix/*` | Emergency production fixes | None (local only) | ❌ |
| `bugfix/*` | Bug fixes | None (local only) | ❌ |

## Workflow

### Feature Development

```
1. Create feature branch from dev
   git checkout -b feat/my-feature dev

2. Develop with TDD
   - Write tests first
   - Implement feature
   - Run validation (pre-commit hook)

3. Push and create PR to dev
   git push -u origin feat/my-feature
   gh pr create --base dev --head feat/my-feature

4. CI validates (lint, type, test, security)

5. Code review + merge to dev

6. Feature flows up:
   dev → qa → sit → uat → main
```

### Hotfix (Emergency Production Fix)

```
1. Create hotfix branch from main
   git checkout -b hotfix/critical-fix main

2. Fix the issue + add regression test

3. Push and create PR to main
   git push -u origin hotfix/critical-fix
   gh pr create --base main --head hotfix/critical-fix

4. Fast-track review (1 approval)

5. Merge to main AND backport to dev
   git checkout dev
   git merge hotfix/critical-fix
```

### Bugfix

```
1. Create bugfix branch from dev
   git checkout -b bugfix/fix-login dev

2. Fix the bug + add regression test

3. Push and create PR to dev
   git push -u origin bugfix/fix-login
   gh pr create --base dev --head bugfix/fix-login

4. Merge to dev → flows up like feature
```

## Merge Flow

```
feat/* ──────→ dev ──────→ qa ──────→ sit ──────→ uat ──────→ main
                  │          │          │           │           │
                  ▼          ▼          ▼           ▼           ▼
               CI Pass    CI Pass   CI Pass     CI Pass     CI Pass
               1 Review   1 Review  1 Review    2 Reviews   2 Reviews
```

## Approval Rules

| Target Branch | Required Approvals | CI Required | Auto-merge |
|---------------|-------------------|-------------|------------|
| dev | 1 | ✅ | ❌ |
| qa | 1 | ✅ | ❌ |
| sit | 1 | ✅ | ❌ |
| uat | 1 | ✅ | ❌ |
| main | 2 | ✅ | ❌ |

## Agent Workflow

### แปะ Spec → Auto Flow

```
1. แปะ spec: .hermes/specs/my-feature.md

2. Agent process:
   - สร้าง plan
   - สร้าง feat/* branch จาก dev
   - ลุย TDD
   - Validate → Commit → Push
   - สร้าง PR → dev

3. CI ทำงานอัตโนมัติ

4. Reviewer ทำการ review

5. Merge → dev → qa → sit → uat → main
```

### Manual Commands

```bash
# Create feature branch
git checkout -b feat/my-feature dev

# Push and create PR
git push -u origin feat/my-feature
gh pr create --base dev --head feat/my-feature --title "feat: my feature" --body "..."

# Check PR status
gh pr view

# Merge (after approval)
gh pr merge --merge

# Backport hotfix to dev
git checkout dev
git merge hotfix/critical-fix
git push
```

## Branch Protection Rules (GitHub)

### main
- Require pull request before merging
- Require 2 approvals
- Require status checks: CI
- Require branches to be up to date
- Restrict who can push (admins only)

### uat
- Require pull request before merging
- Require 1 approval
- Require status checks: CI
- Require branches to be up to date

### sit
- Require pull request before merging
- Require 1 approval
- Require status checks: CI
- Require branches to be up to date

### qa
- Require pull request before merging
- Require 1 approval
- Require status checks: CI
- Require branches to be up to date

### dev
- Require pull request before merging
- Require 1 approval
- Require status checks: CI
- Require branches to be up to date

## Environment Deployments

| Branch | Trigger | Deploy To |
|--------|---------|-----------|
| dev | Push to dev | Dev server |
| qa | Push to qa | QA server |
| sit | Push to sit | SIT server |
| uat | Push to uat | UAT server |
| main | Push to main | Production |

---

*Last updated: 2026-08-27*
