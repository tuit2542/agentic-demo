#!/usr/bin/env bash
# setup.sh — One-click setup for agentic-demo looper
# Usage: ./scripts/setup.sh    (run from repo root, after clone)
set -euo pipefail

echo "🚀 Agentic Demo — Setup"
echo "========================"

# 1. Env
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✅ .env created (from .env.example)"
else
  echo "ℹ️  .env already exists — skip"
fi

# 2. Backend
echo ""
echo "📦 Backend..."
if [ ! -d backend/.venv ]; then
  python -m venv backend/.venv
  echo "✅ venv created"
fi

# activate + install (works on Git Bash / Linux / macOS)
# shellcheck disable=SC1091
if [ -f backend/.venv/Scripts/activate ]; then
  source backend/.venv/Scripts/activate  # Windows Git Bash
else
  source backend/.venv/bin/activate      # Linux/macOS
fi

# Use venv pip directly (more reliable than relying on PATH)
if [ -f backend/.venv/Scripts/python.exe ]; then
  PY="backend/.venv/Scripts/python.exe"
else
  PY="backend/.venv/bin/python"
fi

"$PY" -m pip install -q -r backend/requirements.txt
echo "✅ backend deps installed"

# Validate backend (non-blocking — just report)
echo ""
echo "🔍 Validating backend..."
"$PY" -m ruff check backend/src/ backend/tests/ 2>&1 | tail -2 || true
"$PY" -m mypy backend/src/ --ignore-missing-imports 2>&1 | tail -2 || true
"$PY" -m pytest backend/tests/ -q 2>&1 | tail -2 || true

# 3. Frontend
echo ""
echo "📦 Frontend..."
if [ ! -d frontend/node_modules ]; then
  (cd frontend && npm install --silent)
  echo "✅ frontend deps installed"
else
  echo "ℹ️  frontend/node_modules exists — skip (run: cd frontend && npm install)"
fi

echo ""
echo "🔍 Validating frontend..."
(cd frontend && npx tsc --noEmit 2>&1 | tail -2 || true)
(cd frontend && npm run lint 2>&1 | tail -2 || true)

echo ""
echo "✅ Setup done!"
echo ""
echo "Next steps:"
echo "  1. Edit AGENTS.md — change 'Project Goal' to your project"
echo "  2. cp .hermes/specs/TEMPLATE.md .hermes/specs/my-feature.md  (write spec)"
echo "  3. agy -p \"\$(cat docs/AI_PROMPT_TEMPLATE.md)\" --dangerously-skip-permissions"
echo ""
echo "Or run dev now:"
echo "  backend:  $PY -m uvicorn src.app:create_app --factory --reload --port 8000  (cd backend)"
echo "  frontend: npm run dev  (cd frontend)"
echo "  docs:     cat docs/BOOTSTRAP.md"
