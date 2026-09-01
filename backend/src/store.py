from __future__ import annotations

import random
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone

from src.models import ClickRecord


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    created_at: str


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, email: str, password_hash: str) -> User: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None: ...


class UrlStore:
    def __init__(self) -> None:
        self._urls: dict[str, str] = {}
        self._clicks: dict[str, int] = {}
        self._history: dict[str, list[ClickRecord]] = {}
        self._url_owner: dict[str, int] = {}

    def shorten(
        self, url: str, user_id: int | None = None, custom_id: str | None = None
    ) -> str:
        if custom_id:
            if custom_id in self._urls:
                raise ValueError("Custom ID already taken")
            sid = custom_id
        else:
            sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
            while sid in self._urls:
                sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        self._urls[sid] = url
        self._clicks[sid] = 0
        self._history[sid] = []
        if user_id is not None:
            self._url_owner[sid] = user_id
        return sid

    def resolve(self, sid: str) -> str | None:
        if sid in self._urls:
            self.record_click(sid)
            return self._urls[sid]
        return None

    def record_click(self, sid: str, referrer: str | None = None) -> ClickRecord:
        rec = ClickRecord(
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            referrer=referrer,
        )
        if sid not in self._history:
            self._history[sid] = []
        self._history[sid].append(rec)
        if sid in self._clicks:
            self._clicks[sid] += 1
        return rec

    def get_history(self, sid: str) -> list[ClickRecord]:
        return self._history.get(sid, [])

    def peek(self, sid: str) -> str | None:
        return self._urls.get(sid)

    def stats(self, sid: str) -> int:
        return self._clicks.get(sid, 0)

    def get_owner(self, sid: str) -> int | None:
        return self._url_owner.get(sid)


class InMemoryUserRepo(UserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._by_id: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, email: str, password_hash: str) -> User:
        if email in self._users:
            raise ValueError("Email already registered")
        user = User(
            id=self._next_id,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self._users[email] = user
        self._by_id[user.id] = user
        self._next_id += 1
        return user

    def get_by_email(self, email: str) -> User | None:
        return self._users.get(email)

    def get_by_id(self, user_id: int) -> User | None:
        return self._by_id.get(user_id)
