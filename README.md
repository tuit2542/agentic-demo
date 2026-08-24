# URL Shortener API

## Overview
Simple in-memory URL shortener demonstrating Agentic Full-Loop Engineering.

## Quick Start
```bash
pip install -r requirements.txt
python -m pytest
python src/main.py
```

## API Endpoints
- `POST /shorten` — Create short URL from long URL
- `GET /<short_id>` — Redirect to original URL
- `GET /stats/<short_id>` — View click count

## Development
This project demonstrates the full agentic development loop:
1. Plan (`.hermes/plans/`)
2. Implement (TDD)
3. Review (pre-commit verification)
4. Debug (systematic debugging)
5. CI/CD (GitHub PR workflow)
6. Ship (merge + monitor)
