# Pull Request Template

---

## Description
<!-- อธิบายว่า PR นี้ทำอะไร -->

## Type of Change
<!-- เลือก -->
- [ ] feat: New feature
- [ ] fix: Bug fix
- [ ] docs: Documentation update
- [ ] refactor: Code refactoring
- [ ] ci: CI/CD changes
- [ ] chore: Maintenance

## Checklist
<!-- ติ๊กทุกข้อก่อน submit -->

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] No new warnings

### Testing
- [ ] Tests added/updated
- [ ] All tests pass locally (`pytest tests/ -v`)
- [ ] Coverage maintained or improved

### Documentation
- [ ] `docs/API.md` updated (if API changed)
- [ ] `docs/CHANGELOG.md` updated
- [ ] `docs/HANDOFF.md` updated (if context changed)
- [ ] `docs/WORKFLOW.md` updated (if flow changed)

### CI/CD
- [ ] Lint passes (`ruff check src/ tests/`)
- [ ] Format passes (`ruff format --check src/ tests/`)
- [ ] Type check passes (`mypy src/ --ignore-missing-imports`)
- [ ] Security scan passes (`pip-audit --desc`)

## Breaking Changes
<!-- มี breaking change ไหม -->
- [ ] Yes
- [ ] No

## Related Issues
<!-- link ไป issue ที่เกี่ยวข้อง -->
Closes #

## Screenshots
<!-- ถ้ามี UI change -->
