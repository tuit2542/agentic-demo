# Feature: SQLite Storage

priority: P0
status: ready
created: 2026-08-31
author: ai-generated

## User Story
As a system, I want URL mappings persisted to SQLite so that data survives restarts.

## UI Mockup
N/A — backend only, no UI change.

## API Contract
No API change — existing endpoints keep same contract. Persistence is internal.

### Pydantic Models
No model change. Store persists existing `ClickRecord`.

## Acceptance Criteria
- [ ] AC-1: Given SQLite store, when shorten("https://example.com") then resolve returns same URL
- [ ] AC-2: Given SQLite store, when resolve called twice then stats == 2 and history length == 2
- [ ] AC-3: Given two UrlStore instances sharing same DB file, when first shortens URL then second can resolve it (persistence)
- [ ] AC-4: Given DATABASE_URL env (e.g. `sqlite:///./data.db`), app uses SQLite store; otherwise in-memory
- [ ] AC-5: Given SQLite store, when unknown short_id then resolve returns None, stats 0, history []

## Store Changes
| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| create | `shorten(url)` | `str` | `str` (short_id) |
| read | `resolve(short_id)` | `str` | `str \| None` |
| read | `stats(short_id)` | `str` | `int` |
| read | `get_history(short_id)` | `str` | `list[ClickRecord]` |
| create | `record_click(short_id, referrer?)` | `str` | `ClickRecord` |

Schema: `docs/DATABASE_SCHEMA.md` (urls + clicks tables).

## Files to Modify
- [ ] `backend/src/store_sqlite.py` — new SQLite implementation
- [ ] `backend/src/store.py` — keep InMemory, extract shared interface
- [ ] `backend/src/config.py` — add `get_database_url()`
- [ ] `backend/src/app.py` — select store based on DATABASE_URL
- [ ] `backend/tests/test_store_sqlite.py` — SQLite store tests
- [ ] `backend/tests/test_store.py` — keep in-memory tests

## TDD Checklist
- [ ] Write failing tests first (RED)
- [ ] Minimal implementation (GREEN)
- [ ] Refactor (REFACTOR)
- [ ] All quality gates pass

## Out of Scope
- PostgreSQL migration
- URL expiration
- Custom short ID
