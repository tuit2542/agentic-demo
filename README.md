# Agentic Demo

> URL Shortener — AI-Driven Full-Loop Engineering Demo

[![CI](https://github.com/tuit2542/agentic-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/tuit2542/agentic-demo/actions/workflows/ci.yml)

---

## Overview

Monorepo สำหรับ demo ว่า AI agent สามารถทำ full development loop ได้จริง — จาก spec → TDD → code → validate → deploy

## Tech Stack

| Layer | Stack |
|-------|-------|
| Backend | Python 3.11, FastAPI, Pydantic v2, uvicorn |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS |
| Testing | pytest (16 tests), Vitest (4 tests) |
| CI/CD | GitHub Actions, auto-promote (dev→qa→sit→uat→main) |
| Container | Docker, docker-compose |

## Quick Start

### ใช้ Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### ใช้ Manual

**Backend:**
```bash
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
python -m uvicorn src.app:create_app --factory --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
agentic-demo/
├── backend/              # FastAPI URL shortener
│   ├── src/
│   │   ├── app.py        # FastAPI app + routes
│   │   ├── models.py     # Pydantic models
│   │   └── store.py      # In-memory URL store
│   ├── tests/            # 16 tests (pytest)
│   ├── scripts/          # Validation scripts
│   └── Dockerfile
├── frontend/             # Next.js UI
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx  # URL shortener form
│   │   │   └── layout.tsx
│   │   └── lib/
│   │       └── api.ts    # API client
│   └── Dockerfile
├── docs/                 # Documentation
├── .hermes/              # AI agent config
├── docker-compose.yml    # Full stack
└── AGENTS.md             # Agent instructions
```

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/shorten` | POST | Create short URL |
| `/stats/{sid}` | GET | Get click stats |
| `/{sid}` | GET | Redirect to original URL |

Full API docs: http://localhost:8000/docs

## For AI Agents

1. Read `AGENTS.md` — project rules
2. Read `docs/TRACKING.md` — feature checklist
3. Copy `.hermes/specs/TEMPLATE.md` → fill spec
4. TDD: RED → GREEN → REFACTOR
5. Validate → Commit → Auto-Promote

## Validation

```bash
# Backend
cd backend && python scripts/pre_commit_validate.py

# Frontend
cd frontend && npm run lint && npx tsc --noEmit && npm run test
```

## Branching

```
feat/* → dev → qa → sit → uat → main
```

Auto-promote: merge to dev → ไปถึง main อัตโนมัติ

## License

MIT
