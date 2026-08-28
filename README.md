# Agentic Demo — Monorepo

## Structure
```
├── backend/           ← Python FastAPI
│   ├── src/
│   ├── tests/
│   ├── scripts/
│   └── requirements.txt
├── frontend/          ← Next.js 16 + React 19 + TypeScript
│   ├── src/
│   │   ├── app/       ← App Router pages
│   │   ├── components/
│   │   ├── types/
│   │   ├── lib/       ← API clients
│   │   └── __tests__/
│   └── package.json
├── docs/              ← Documentation
├── .hermes/           ← Agent config
├── .hermes.md         ← Project rules
├── AGENTS.md          ← Agent instructions
└── docker-compose.yml
```

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.app:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Commands

### Backend
| Command | Description |
|---------|-------------|
| `cd backend && python -m pytest tests/ -v` | Run tests |
| `cd backend && python scripts/pre_commit_validate.py` | Validate |
| `cd backend && ruff check src/ tests/` | Lint |
| `cd backend && mypy src/ --ignore-missing-imports` | Type check |

### Frontend
| Command | Description |
|---------|-------------|
| `cd frontend && npm run dev` | Dev server |
| `cd frontend && npm run build` | Build |
| `cd frontend && npm run test` | Test |
| `cd frontend && npm run lint` | Lint |
| `cd frontend && npx tsc --noEmit` | Type check |

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.11, FastAPI, Pydantic v2 |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS |
| Testing | pytest (backend), Vitest (frontend) |
| Linting | ruff (backend), ESLint (frontend) |
| Type check | mypy (backend), TypeScript (frontend) |
