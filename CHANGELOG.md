# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Best practices registry (`.hermes/best-practices.md`)
- Spec intake pipeline with auto-detect
- Pre-commit validation pipeline (language-agnostic)
- Project health monitor cron job with continuity
- Agentic workflow user guide (`AGENTIC_WORKFLOW.md`)

### Changed
- Migrated from Flask to FastAPI with async endpoints
- Validation config now auto-detects project language

## [0.2.0] - 2026-08-26

### Added
- Pydantic v2 models with type validation
- FastAPI async endpoints (POST /shorten, GET /<id>, GET /stats/<id>)
- Async test client with httpx
- mypy type checking in validation pipeline

### Changed
- Migrated from Flask to FastAPI
- Updated test suite for async compatibility

## [0.1.0] - 2026-08-26

### Added
- Initial Flask URL shortener implementation
- In-memory URL store with click tracking
- Basic test suite (pytest)
- Linting with ruff
- Git repository setup with conventional commits
