# AI Feature Implementation Prompt Template

> ใช้ template นี้สั่งงาน AI agent (agy, Claude Code, Codex, etc.)

---

## Template

```
Read these files first:
1. .hermes/specs/{FEATURE_NAME}.md (the feature spec)
2. AGENTS.md (project rules + commands)
3. backend/.hermes.md (backend rules) — if backend feature
4. frontend/.hermes.md (frontend rules) — if frontend feature

IMPLEMENTATION STEPS:

Step 1 — RED (Write failing tests FIRST):
- Read current code: backend/src/models.py, backend/src/store.py, backend/src/app.py
- Read current tests: backend/tests/test_models.py, backend/tests/test_store.py, backend/tests/test_app.py
- Write failing tests for each Acceptance Criteria in the spec
- Run: cd backend && python -m pytest tests/ -v
- Verify tests FAIL (RED phase)

Step 2 — GREEN (Minimal implementation):
- Implement minimum code to make tests pass
- Do NOT add features beyond the spec
- Run: cd backend && python -m pytest tests/ -v
- Verify all tests PASS (GREEN phase)

Step 3 — REFACTOR (Clean up):
- Remove duplication
- Improve naming
- Run: cd backend && python -m pytest tests/ -v
- Verify tests still PASS

Step 4 — Validation:
- Run: cd backend && python -m ruff check src/ tests/
- Run: cd backend && python -m mypy src/ --ignore-missing-imports
- Run: cd backend && python -m pytest tests/ -v

Step 5 — Update docs:
- Update docs/CHANGELOG.md under [Unreleased]
- Update docs/API.md if new endpoints

RULES:
- Follow TDD strictly: RED → GREEN → REFACTOR
- Type hints on all public functions
- Pydantic models for all request/response
- Test all error paths
- No wildcard imports
- Use Conventional Commits: feat: or fix:
```

---

## Example (Click Analytics)

```
Read these files first:
1. .hermes/specs/click-analytics.md
2. AGENTS.md
3. backend/.hermes.md

IMPLEMENTATION STEPS:

Step 1 — RED:
- Add ClickRecord model to tests/test_models.py
- Add test_record_click_returns_click_record to tests/test_store.py
- Add test_get_history_returns_clicks to tests/test_store.py
- Add test_stats_returns_history to tests/test_app.py
- Run: cd backend && python -m pytest tests/ -v
- Verify FAIL

Step 2 — GREEN:
- Add ClickRecord to src/models.py
- Add clicks_history to store
- Add record_click, get_history methods
- Update stats endpoint
- Run: cd backend && python -m pytest tests/ -v
- Verify PASS

Step 3 — REFACTOR + VALIDATION + DOCS
```

---

## Quick Reference

| AI Agent | Command |
|----------|---------|
| agy | `agy -p "PROMPT" --dangerously-skip-permissions` |
| Claude Code | `claude -p "PROMPT" --dangerously-skip-permissions` |
| Codex | `codex --approval-mode full-auto "PROMPT"` |
| Hermes | `delegate_task` with goal + context |

---

## Tips
- เลือก feature ที่ scope ชัดเจน — ไม่กว้างเกินไป
- ระบุ files ที่ต้องแก้ — AI จะไม่เดา
- ระบุ test cases ชัดเจน — AI จะเขียน tests ได้ตรง
- ตั้ง timeout ให้พอ (300-600s) — TDD loop ใช้เวลา
- เช็ค tests หลัง AI เสร็จ — บางที AI ข้าม validation
