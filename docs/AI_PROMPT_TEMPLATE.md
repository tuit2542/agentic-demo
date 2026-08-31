# AI Feature Implementation Prompt Template

> ใช้ template นี้สั่งงาน AI agent (agy, Claude Code, Codex, etc.)
> AI จะทำ full-loop: design → code → test → commit → push → PR

---

## Template (Full Loop)

```
Read these files first:
1. .hermes/specs/{FEATURE_NAME}.md (the feature spec)
2. AGENTS.md (project rules + commands)
3. backend/.hermes.md (backend rules) — if backend feature
4. frontend/.hermes.md (frontend rules) — if frontend feature

IMPLEMENTATION STEPS (FULL LOOP):

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

Step 4 — Validation (ALL must pass):
- Run: cd backend && python -m ruff check src/ tests/
- Run: cd backend && python -m mypy src/ --ignore-missing-imports
- Run: cd backend && python -m pytest tests/ -v
- If ANY check fails → fix it before proceeding

Step 5 — Update docs:
- Update docs/CHANGELOG.md under [Unreleased]
- Update docs/API.md if new endpoints

Step 6 — Commit & Push (DO NOT SKIP):
- git add -A
- git commit -m "feat: {FEATURE_NAME} — short description"
  (or "fix:" if bug fix, "chore:" if non-src change)
- git push -u origin HEAD

Step 7 — Create PR:
- gh pr create --title "feat: {FEATURE_NAME}" --body "## Changes
- Summary of what was implemented
- List key files changed

## Verification
- Backend: N tests passed ✅
- Frontend: M tests passed ✅ (if applicable)
- Type check: passed ✅"

RULES:
- Follow TDD strictly: RED → GREEN → REFACTOR
- Type hints on all public functions
- Pydantic models for all request/response
- Test all error paths
- No wildcard imports
- Use Conventional Commits: feat: or fix:
- ALWAYS commit + push + create PR at the end
- NEVER stop after coding — the loop is not done until PR is created
```

---

## Example (Click Analytics)

```
Read these files first:
1. .hermes/specs/click-analytics.md
2. AGENTS.md
3. backend/.hermes.md

IMPLEMENTATION STEPS (FULL LOOP):

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

Step 6 — COMMIT & PUSH:
- git add -A
- git commit -m "feat: click analytics — add click history tracking"
- git push -u origin HEAD

Step 7 — CREATE PR:
- gh pr create --title "feat: click analytics" --body "..."
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
- **สำคัญ:** ต้องบอกให้ AI commit + push + PR — ถ้าไม่บอกจะไม่ทำ
