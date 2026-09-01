from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import get_jwt_expire_minutes, get_jwt_secret
from src.store import InMemoryUserRepo, UserRepository


def _user_repo_factory() -> UserRepository:
    """Create user repo based on DATABASE_URL env."""
    db_url = os.getenv("DATABASE_URL", "")
    if db_url:
        from src.store_sqlite import SqliteUserRepo

        return SqliteUserRepo(db_url)
    return InMemoryUserRepo()


# Singleton — same repo for all requests
_user_repo: UserRepository | None = None


def get_user_repo() -> UserRepository:
    global _user_repo
    if _user_repo is None:
        _user_repo = _user_repo_factory()
    return _user_repo


security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token(user_id: int, email: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=get_jwt_expire_minutes()),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm="HS256")


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return verify_token(credentials.credentials)
