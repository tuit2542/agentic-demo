from __future__ import annotations

import os


def get_cors_origins() -> list[str]:
    """Read CORS origins from env."""
    raw = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001")
    return [o.strip() for o in raw.split(",") if o.strip()]


def get_base_url() -> str:
    """Base URL for short URLs."""
    return os.getenv("BASE_URL", "http://localhost:8000")


def get_host() -> str:
    return os.getenv("BACKEND_HOST", "0.0.0.0")


def get_port() -> int:
    return int(os.getenv("BACKEND_PORT", "8000"))
