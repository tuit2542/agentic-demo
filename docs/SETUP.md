# Setup & GitHub Integration

> Agentic Demo — Project setup

---

## First Time Setup

```bash
# 1. Clone repo
git clone https://github.com/tuit2542/agentic-demo
cd agentic-demo

# 2. Setup venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install deps
pip install -r requirements.txt

# 4. Verify
pytest tests/ -v
python scripts/pre_commit_validate.py
```

---

## GitHub CLI

```bash
# Login (once)
"/c/Program Files/GitHub CLI/gh.exe" auth login

# Create remote repo
"/c/Program Files/GitHub CLI/gh.exe" repo create agentic-demo --public --source=. --remote=origin --push
```

---

## Branch Protection

Go to: `https://github.com/tuit2542/agentic-demo/settings/branches`

Add rule for each branch: `main`, `uat`, `sit`, `qa`, `dev`

- ✅ Require pull request before merging
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- Status checks: `CI`

---

## GitHub Actions CI

Already configured in `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main, dev, qa, sit, uat]
  pull_request:
    branches: [main, dev, qa, sit, uat]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install -r requirements.txt
      - run: python -m ruff check src/ tests/
      - run: python -m mypy src/ --ignore-missing-imports
      - run: python -m pytest tests/ -v
```

---

## Auto-Promote & Deploy

| Workflow | Trigger | Action |
|----------|---------|--------|
| `ci.yml` | push/PR | lint, type, test, security |
| `auto-promote.yml` | push to env | Create PR to next env |
| `deploy.yml` | push to env | Deploy to environment |

---

## Cron Jobs

| Job ID | Name | Schedule |
|--------|------|----------|
| `e1deadafefd4` | project-health-monitor | every 30m |
| `7eb8fde941a9` | spec-intake-monitor | every 10m |

Scripts must be in `~/.hermes/scripts/` for cron to find them.

---

## Quick Commands

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

---

*Last updated: 2026-08-27*