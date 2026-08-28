# Multi-Language Support

> วิธีใช้ Agentic Demo กับภาษาอื่น

---

## Checklist สำหรับภาษาใหม่

### 1. เพิ่มภาษาใน Validation Config (`.hermes/validation.json`)

```json
{
  "languages": {
    "python": {
      "detect": ["*.py", "requirements.txt", "pyproject.toml"],
      "lint": "python -m ruff check {src}",
      "typecheck": "python -m mypy {src} --ignore-missing-imports",
      "test": "python -m pytest {test} -v",
      "security": "python -m pip-audit --desc || true"
    },
    "typescript": {
      "detect": ["*.ts", "tsconfig.json"],
      "lint": "npx eslint {src}",
      "typecheck": "npx tsc --noEmit",
      "test": "npx vitest run {test}",
      "security": "npm audit || true"
    },
    "go": {
      "detect": ["go.mod"],
      "lint": "golangci-lint run {src}",
      "typecheck": "go vet {src}",
      "test": "go test {test}/... -v",
      "security": "govulncheck ./... || true"
    },
    "rust": {
      "detect": ["Cargo.toml"],
      "lint": "cargo clippy -- -D warnings",
      "typecheck": "cargo check",
      "test": "cargo test {test}",
      "security": "cargo audit || true"
    }
  }
}
```

### 2. แก้ `.hermes.md`

```markdown
## Tech Stack
- **Language:** (เปลี่ยน)
- **Framework:** (เปลี่ยน)
- **Testing:** (เปลี่ยน)

## Build & Test Commands
- Install deps: (เปลี่ยน)
- Run tests: (เปลี่ยน)
- Lint: (เปลี่ยน)
- Type check: (เปลี่ยน)
```

### 3. แก้ dependency file

| Language | File |
|----------|------|
| Python | `requirements.txt` / `pyproject.toml` |
| TypeScript | `package.json` |
| Go | `go.mod` |
| Rust | `Cargo.toml` |

### 4. แก้ `.github/workflows/ci.yml`

```yaml
# Python
- uses: actions/setup-python@v5
  with: { python-version: "3.11" }

# TypeScript
- uses: actions/setup-node@v4
  with: { node-version: "20" }

# Go
- uses: actions/setup-go@v5
  with: { go-version: "1.22" }

# Rust
- uses: dtolnay/rust-toolchain@stable
```

### 5. สร้าง src/ + tests/ structure

```
src/           ← Source code
tests/         ← Tests (mirror src/ structure)
```

---

## ไม่ต้องแก้ (ใช้ได้เลย)

- `scripts/pre_commit_validate.py` — auto-detect จาก validation.json
- `.hermes/best-practices.md` — language-agnostic
- `.hermes/specs/` — แค่ markdown
- Branching strategy
- Auto-promote/deploy workflows

---

## ตัวอย่างภาษา

### TypeScript

```json
{
  "languages": {
    "typescript": {
      "detect": ["*.ts", "tsconfig.json", "package.json"],
      "lint": "npx eslint {src}",
      "typecheck": "npx tsc --noEmit",
      "test": "npx vitest run {test}",
      "security": "npm audit || true"
    }
  }
}
```

```yaml
# .github/workflows/ci.yml
- uses: actions/setup-node@v4
  with: { node-version: "20" }
- run: npm ci
- run: npx eslint src/
- run: npx tsc --noEmit
- run: npx vitest run
```

### Go

```json
{
  "languages": {
    "go": {
      "detect": ["go.mod"],
      "lint": "golangci-lint run {src}",
      "typecheck": "go vet {src}",
      "test": "go test {test}/... -v",
      "security": "govulncheck ./... || true"
    }
  }
}
```

```yaml
# .github/workflows/ci.yml
- uses: actions/setup-go@v5
  with: { go-version: "1.22" }
- run: golangci-lint run ./...
- run: go vet ./...
- run: go test ./... -v
```

### Rust

```json
{
  "languages": {
    "rust": {
      "detect": ["Cargo.toml"],
      "lint": "cargo clippy -- -D warnings",
      "typecheck": "cargo check",
      "test": "cargo test {test}",
      "security": "cargo audit || true"
    }
  }
}
```

```yaml
# .github/workflows/ci.yml
- uses: dtolnay/rust-toolchain@stable
  with:
    components: clippy, rustfmt
- run: cargo clippy -- -D warnings
- run: cargo check
- run: cargo test --verbose
```

---

*Last updated: 2026-08-27*