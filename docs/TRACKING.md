# Feature Tracking Checklist

> ทำตาม checklist นี้ทุกครั้งเมื่อเริ่ม feature ใหม่

---

## Before You Start

- [ ] อ่าน `AGENTS.md` (agent rules + commands)
- [ ] อ่าน `.hermes.md` (project rules)
- [ ] อ่าน `backend/.hermes.md` (backend-specific rules)
- [ ] อ่าน `frontend/.hermes.md` (frontend-specific rules)
- [ ] อ่าน `docs/ERROR_HANDLING.md` (error patterns)
- [ ] อ่าน `docs/DATABASE_SCHEMA.md` (data layer — current: in-memory dict)
- [ ] Copy `.hermes/specs/TEMPLATE.md` → `.hermes/specs/<feature-name>.md`
- [ ] เติม spec: User Story, Acceptance Criteria, UI Mockup, API Contract

## TDD Loop

- [ ] RED: เขียน failing test ตัวแรก
- [ ] GREEN: implement ให้ผ่าน
- [ ] REFACTOR: clean up code
- [ ] Repeat จนครบทุก acceptance criterion

## Validation (ก่อน commit)

- [ ] Backend: `cd backend && python scripts/pre_commit_validate.py`
- [ ] Frontend: `cd frontend && python scripts/validate.py`

## Documentation (หลัง implement)

- [ ] Update `docs/API.md` — add row to Endpoints table + example
- [ ] Update `docs/CHANGELOG.md` — add bullet under `[Unreleased]`
- [ ] Update `docs/HANDOFF.md` — update What's Done table

## Commit & Push

- [ ] Branch name: `feat/<feature-name>` (src code) หรือ `chore/<name>` (non-src)
- [ ] Commit message: Conventional Commits (`feat:`, `fix:`, `chore:`)
- [ ] Push to origin
- [ ] Create PR → target `dev`
- [ ] Auto-Promote: dev → qa → sit → uat → main (อัตโนมัติ)

## Verify

- [ ] CI passes (backend + frontend)
- [ ] PR merged to main
- [ ] Feature works in production

---

## Notes
- **Scratch files:** ห้าม commit
- **Secrets:** ห้าม commit
- **Type hints:** ต้องมีครบ (backend)
- **Tests:** ต้องมีครบ (backend + frontend)
