# GitLab Migration Guide

> วิธีย้าย from GitHub to GitLab

---

## Quick Comparison

| Feature | GitHub | GitLab |
|---------|--------|--------|
| CLI | `gh` | `glab` |
| CI/CD | `.github/workflows/ci.yml` | `.gitlab-ci.yml` |
| Branch protection | Settings → Branch rules | Settings → Protected branches |
| PR | Pull Request | Merge Request |
| API | `api.github.com` | `gitlab.com/api/v4` |
| Runner | GitHub-hosted | Shared/Docker/Self-hosted |

---

## Step 1: Install GitLab CLI

```bash
# Windows
winget install GLab.GLab

# macOS
brew install glab

# Verify
glab --version
```

---

## Step 2: Login

```bash
glab auth login
# เลือก: gitlab.com → HTTPS → Browser หรือ Token
```

---

## Step 3: ย้าย Remote

```bash
cd D:/Users/pongsathornb/agentic-demo

# ลบ GitHub remote
git remote remove origin

# เพิ่ม GitLab remote
git remote add origin https://gitlab.com/your-username/agentic-demo.git

# Push ทุกอย่าง
git push -u origin main --all
git push --tags
```

---

## Step 4: สร้าง `.gitlab-ci.yml`

สร้างไฟล์ `.gitlab-ci.yml` ที่ root:

```yaml
stages:
  - lint
  - test
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

# ==================== LINT ====================
lint:
  stage: lint
  image: python:3.11
  script:
    - pip install ruff mypy
    - ruff check src/ tests/
    - mypy src/ --ignore-missing-imports
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH

# ==================== TEST ====================
test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pytest tests/ -v
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH

# ==================== SECURITY ====================
security:
  stage: security
  image: python:3.11
  allow_failure: true
  script:
    - pip install pip-audit
    - pip-audit --desc
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH

# ==================== AUTO-PROMOTE ====================
promote:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache bash curl
  script:
    - |
      NEXT_ENV=""
      if [ "$CI_COMMIT_BRANCH" = "dev" ]; then
        NEXT_ENV="qa"
      elif [ "$CI_COMMIT_BRANCH" = "qa" ]; then
        NEXT_ENV="sit"
      elif [ "$CI_COMMIT_BRANCH" = "sit" ]; then
        NEXT_ENV="uat"
      elif [ "$CI_COMMIT_BRANCH" = "uat" ]; then
        NEXT_ENV="main"
      fi
      
      if [ -n "$NEXT_ENV" ]; then
        echo "Promoting $CI_COMMIT_BRANCH → $NEXT_ENV"
        glab mr create \
          --source-branch "$CI_COMMIT_BRANCH" \
          --target-branch "$NEXT_ENV" \
          --title "promote: $CI_COMMIT_BRANCH → $NEXT_ENV" \
          --remove-source-branch \
          --yes
      fi
  rules:
    - if: $CI_COMMIT_BRANCH == "dev"
    - if: $CI_COMMIT_BRANCH == "qa"
    - if: $CI_COMMIT_BRANCH == "sit"
    - if: $CI_COMMIT_BRANCH == "uat"

# ==================== DEPLOY ====================
deploy_dev:
  stage: deploy
  script:
    - echo "Deploying to dev environment..."
    # เพิ่ม deploy command
  rules:
    - if: $CI_COMMIT_BRANCH == "dev"

deploy_qa:
  stage: deploy
  script:
    - echo "Deploying to QA environment..."
  rules:
    - if: $CI_COMMIT_BRANCH == "qa"

deploy_sit:
  stage: deploy
  script:
    - echo "Deploying to SIT environment..."
  rules:
    - if: $CI_COMMIT_BRANCH == "sit"

deploy_uat:
  stage: deploy
  script:
    - echo "Deploying to UAT environment..."
  rules:
    - if: $CI_COMMIT_BRANCH == "uat"

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to production..."
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

---

## Step 5: ตั้ง Branch Protection

GitLab: Settings → Protected Branches

| Branch | Protected | Allowed to merge | Allowed to push |
|--------|-----------|------------------|-----------------|
| `main` | ✅ | Maintainers | No one |
| `uat` | ✅ | Maintainers | No one |
| `sit` | ✅ | Maintainers + Developers | No one |
| `qa` | ✅ | Maintainers + Developers | No one |
| `dev` | ✅ | Maintainers + Developers | No one |

---

## Step 6: ลบ GitHub workflows

```bash
rm -rf .github/
git add -A
git commit -m "chore: migrate from GitHub Actions to GitLab CI"
git push
```

---

## Step 7: Update Documentation

```bash
# แก้ docs/SETUP.md
# แก้ docs/INDEX.md
# แก้ docs/WORKFLOW.md
```

---

## Step 8: ย้าย Cron Jobs

Hermes cron ไม่ต้องแก้ — ทำงานกับ local git ได้เลย

---

## Commands Comparison

| Task | GitHub (`gh`) | GitLab (`glab`) |
|------|---------------|-----------------|
| Create repo | `gh repo create` | `glab repo create` |
| Create PR/MR | `gh pr create` | `glab mr create` |
| List PRs/MRs | `gh pr list` | `glab mr list` |
| Merge | `gh pr merge` | `glab mr merge` |
| View CI | `gh run list` | `glab ci list` |
| View logs | `gh run view` | `glab ci view` |

---

## Migration Checklist

```
□ Install glab CLI
□ glab auth login
□ git remote add origin (GitLab)
□ git push --all + --tags
□ สร้าง .gitlab-ci.yml
□ ลบ .github/workflows/
□ ตั้ง branch protection (GitLab Settings)
□ Update .hermes.md (GitLab commands)
□ Update docs/SETUP.md
□ ทดสอบ CI pipeline
□ Verify auto-promote works
□ Verify auto-deploy works
```

---

*Last updated: 2026-08-27*