# Feature: JWT Authentication

priority: P1
status: ready
created: 2026-09-01
author: ai-generated

## User Story
As a system owner, I want API authentication so that only authorized users can create short URLs and access analytics.

## UI Mockup
N/A — backend only. Login/register endpoints + auth middleware.

## API Contract

### Endpoint: `POST /auth/register`
```
Request:
  Body: { "email": "string", "password": "string" }

Response 201:
  { "id": 1, "email": "user@example.com", "created_at": "2026-09-01T10:00:00Z" }

Response 422:
  { "detail": "Email already registered" }
```

### Endpoint: `POST /auth/login`
```
Request:
  Body: { "email": "string", "password": "string" }

Response 200:
  { "access_token": "eyJ...", "token_type": "bearer" }

Response 401:
  { "detail": "Invalid credentials" }
```

### Protected Endpoints
```
POST /shorten  — requires Authorization: Bearer <token>
GET  /<id>     — public (redirect, no auth)
GET  /stats/{sid} — requires auth (own URLs only)
GET  /health   — public
```

## Acceptance Criteria
- [ ] AC-1: Given valid email+password, when POST /auth/register, then 201 + user created
- [ ] AC-2: Given registered user, when POST /auth/login with correct credentials, then JWT token returned
- [ ] AC-3: Given invalid password, when POST /auth/login, then 401 returned
- [ ] AC-4: Given valid JWT, when POST /shorten, then 201 returned (URL owned by user)
- [ ] AC-5: Given no JWT or invalid JWT, when POST /shorten, then 401 returned
- [ ] AC-6: Given JWT, when GET /stats/{sid}, then only stats for URLs owned by user
- [ ] AC-7: Given JWT, when GET /{sid}, then redirect works (public, no auth needed)

## Store Changes
| Operation | Method | Input | Output |
|-----------|--------|-------|--------|
| create user | `store.create_user(email, password_hash)` | `str` | `User` |
| get user | `store.get_user_by_email(email)` | `str` | `User \| None` |
| associate url | urls table gets `user_id` FK |

## Files to Modify
- [ ] `backend/src/auth.py` — new: JWT utils, password hashing, dependencies
- [ ] `backend/src/store.py` — add user methods
- [ ] `backend/src/store_sqlite.py` — add users table + user methods
- [ ] `backend/src/models.py` — add User model
- [ ] `backend/src/app.py` — add auth routes, protect /shorten + /stats
- [ ] `backend/src/config.py` — add JWT_SECRET, JWT_EXPIRE_MINUTES
- [ ] `backend/tests/test_auth.py` — new
- [ ] `backend/tests/test_app.py` — update for auth
- [ ] `backend/requirements.txt` — add bcrypt, pyjwt

## TDD Checklist
- [ ] Write failing tests first (RED)
- [ ] Minimal implementation (GREEN)
- [ ] Refactor (REFACTOR)
- [ ] All quality gates pass

## Out of Scope
- OAuth / social login
- Role-based access control
- Token refresh endpoint
- API key authentication
