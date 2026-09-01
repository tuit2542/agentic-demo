# SQLite Store Implementation

Read ALL of these files before starting:
- backend/src/store.py (current in-memory store)
- backend/src/app.py (how store is used)
- backend/src/models.py (ClickRecord, etc.)
- backend/src/config.py (existing config)
- docs/DATABASE_SCHEMA.md (schema to follow)
- backend/tests/test_store.py (existing tests)
- backend/tests/test_app.py (existing tests)

## Your Task
Implement a SQLite-backed store in `backend/src/store_sqlite.py`.

## Requirements
1. Follow the EXACT schema in docs/DATABASE_SCHEMA.md (urls + clicks tables)
2. Implement same interface as UrlStore: shorten(), resolve(), stats(), get_history(), record_click()
3. Use sqlite3 stdlib (no extra dependencies)
4. Auto-create tables on first connection
5. Add get_database_url() to backend/src/config.py (env: DATABASE_URL)
6. Update backend/src/app.py: if DATABASE_URL set, use SqliteStore; else use UrlStore
7. Write tests in backend/tests/test_store_sqlite.py (follow test_store.py pattern)
8. Keep ALL existing tests passing (do NOT break UrlStore)

## TDD
- RED: write test_store_sqlite.py tests FIRST
- GREEN: implement store_sqlite.py
- REFACTOR: clean up

## Quality Gates (run all before finishing)
- cd backend && python -m pytest tests/ -v
- cd backend && python -m ruff check src/ tests/
- cd backend && python -m mypy src/ --ignore-missing-imports

## Push
- Commit: feat/sqlite-storage
- Create PR to dev
