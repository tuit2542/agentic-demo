# Feature: [NAME]

---
spec_id: [auto-generated]
priority: P0 | P1 | P2
status: draft | ready | in_progress | done
created: [YYYY-MM-DD]
author: [name or "ai-generated"]
---

## User Story
As a [user type], I want [goal] so that [benefit].

## UI Mockup
> Paste image URL or local path below. AI must follow this layout.

![UI Mockup](path/to/mockup.png)

### Layout Rules (AI MUST follow)
- Components: [list key components from mockup]
- Colors: [primary, secondary, background]
- Responsive: mobile-first | desktop-first

## API Contract

### Endpoint: `[METHOD] /path`
```
Request:
  Body: { "field": "type" }
  
Response 200:
  { "field": "type" }

Response 4xx:
  { "detail": "error message" }
```

### Pydantic Models
```python
class RequestModel(BaseModel):
    field: type

class ResponseModel(BaseModel):
    field: type
```

## Acceptance Criteria
> Format: Given [context], when [action], then [outcome]
> Each criterion MUST be testable.

- [ ] AC-1: Given [context], when [action], then [outcome]
- [ ] AC-2: Given [context], when [action], then [outcome]
- [ ] AC-3: Given [context], when [action], then [outcome]

## Store Changes
> What changes to the data layer are needed?

| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| [create/read/update/delete] | `store.method()` | `type` | `type` |

## Files to Modify
- [ ] `src/models.py` — add/update Pydantic models
- [ ] `src/store.py` — add/update store methods
- [ ] `src/app.py` — add/update endpoints
- [ ] `tests/test_models.py` — model tests
- [ ] `tests/test_store.py` — store tests
- [ ] `tests/test_app.py` — endpoint tests

## TDD Checklist
- [ ] Write failing tests first (RED)
- [ ] Minimal implementation (GREEN)
- [ ] Refactor (REFACTOR)
- [ ] All 6 quality gates pass

## Out of Scope
- What this feature does NOT include
