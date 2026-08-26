# Best Practices Registry
# Agent จะอ่านไฟล์นี้ก่อนเริ่ม task ทุกครั้ง

## Core Principles
1. TDD is non-negotiable — test first, then implement
2. Type safety — type hints on all public functions
3. Validate before commit — lint + type check + test
4. Small focused changes — one feature per commit
5. Defensive coding — handle errors explicitly

## Language-Specific Rules
<!-- Agent auto-loads rules ตาม language ที่ detect ได้ -->

### Python
- Style: ruff (line-length=88)
- Type check: mypy (strict mode optional)
- Tests: pytest with asyncio
- Imports: no wildcard imports
- Path: prefer pathlib over os.path

### JavaScript / TypeScript
- Style: eslint + prettier
- Type check: tsc --noEmit (strict)
- Tests: vitest or jest
- Imports: prefer named exports
- Async: async/await over .then()

### Rust
- Style: cargo fmt
- Lint: cargo clippy -D warnings
- Tests: cargo test (unit + integration)
- Error handling: use anyhow or thiserror
- Memory: prefer borrowing over cloning

### Go
- Style: gofmt + goimports
- Lint: golangci-lint
- Tests: go test ./...
- Error handling: check every error
- Naming: Go conventions (camelCase exports)

## Workflow Rules
1. Always read .hermes.md before starting
2. Always read AGENTS.md for project context
3. Run validation pipeline before every commit
4. Use conventional commits format
5. One concern per file, one feature per commit

## Quality Gates
| Gate | Command | Must Pass |
|------|---------|-----------|
| Lint | (from validation.json) | ✅ |
| Type check | (from validation.json) | ✅ |
| Tests | (from validation.json) | ✅ |

## Anti-Patterns
- ❌ Skipping tests
- ❌ Large commits
- ❌ Mixing concerns
- ❌ Guessing when debugging
- ❌ Hardcoding values that should be config

## Security
- Never commit secrets or API keys
- Validate all external inputs
- Use environment variables for config
- Scan for vulnerabilities before release

## Documentation
- Every public function has docstring
- README.md updated with new features
- CHANGELOG.md for version history
- ADR (Architecture Decision Records) for major decisions
