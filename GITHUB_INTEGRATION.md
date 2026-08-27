# GitHub Integration Guide

เชื่อม agentic workflow กับ GitHub

---

## 1. Login (ทำครั้งเดียว)

```bash
"/c/Program Files/GitHub CLI/gh.exe" auth login
```

เลือก:
- **GitHub.com**
- **HTTPS**
- **Login with browser**

## 2. สร้าง Remote Repo

```bash
cd D:/Users/pongsathornb/agentic-demo

"/c/Program Files/GitHub CLI/gh.exe" repo create agentic-demo --public --source=. --remote=origin --push
```

## 3. Push

```bash
git push -u origin main
git push --tags
```

## 4. ตั้ง Branch Protection

ไปที่: `https://github.com/<username>/agentic-demo/settings/branches`

เพิ่ม rule สำหรับ `main`:
- ✅ Require pull request before merging
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- Status checks: `lint`, `type-check`, `test`

## 5. ตั้ง GitHub Actions CI

สร้างไฟล์ `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint
        run: python -m ruff check src/ tests/

      - name: Type check
        run: python -m mypy src/ --ignore-missing-imports

      - name: Tests
        run: python -m pytest tests/ -v
```

## 6. Full Workflow หลังจากเชื่อม GitHub

```
1. แปะ spec → .hermes/specs/
2. Agent process (auto-detect cron)
3. Agent สร้าง plan → TDD → validate
4. Agent สร้าง branch: feat/<name>
5. Agent commit + push
6. CI validate อัตโนมัติ
7. Agent สร้าง PR
8. Review → Merge
```

## Quick Commands

```bash
# ดู repos
"/c/Program Files/GitHub CLI/gh.exe" repo list

# ดู PRs
"/c/Program Files/GitHub CLI/gh.exe" pr list

# ดู CI status
"/c/Program Files/GitHub CLI/gh.exe" run list

# สร้าง PR
"/c/Program Files/GitHub CLI/gh.exe" pr create --title "feat: ..." --body "..."
```
