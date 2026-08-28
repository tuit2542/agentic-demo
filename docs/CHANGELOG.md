# Changelog

> Agentic Demo — Version history

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

---

## [Unreleased]

### Added
- Documentation split into multiple files (docs/)
- Auto-update flow in .hermes.md

### Changed
- Consolidated all docs from PROJECT_DOCS.md to docs/

---

## [0.2.0] - 2026-08-26

### Added
- Pydantic v2 models with type validation
- FastAPI async endpoints (POST /shorten, GET /<id>, GET /stats/<id>)
- Async test client with httpx
- mypy type checking in validation pipeline
- Language-agnostic validation config
- Pre-commit validation pipeline
- Spec intake pipeline with auto-detect
- Project health monitor cron job with continuity
- Best practices registry

### Changed
- Migrated from Flask to FastAPI
- Validation config now auto-detects project language

---

## [0.1.0] - 2026-08-26

### Added
- Initial Flask URL shortener implementation
- In-memory URL store with click tracking
- Basic test suite (pytest)
- Linting with ruff
- Git repository setup with conventional commits

---

*Last updated: 2026-08-27*