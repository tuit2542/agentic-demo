from __future__ import annotations

import random
import sqlite3
import string
from datetime import datetime, timezone

from src.models import ClickRecord
from src.store import User, UserRepository


class SqliteStore:
    """SQLite-backed URL store."""

    def __init__(self, db_path: str = "urlshortener.db") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS urls (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id    TEXT NOT NULL UNIQUE,
                original_url TEXT NOT NULL,
                user_id     INTEGER REFERENCES users(id),
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_short_id ON urls(short_id);

            CREATE TABLE IF NOT EXISTS clicks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                url_id      INTEGER NOT NULL REFERENCES urls(id),
                clicked_at  TEXT NOT NULL DEFAULT (datetime('now')),
                referrer    TEXT DEFAULT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_url_id ON clicks(url_id);
            """
        )
        self._conn.commit()

    def shorten(self, url: str, user_id: int | None = None) -> str:
        sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        while self._get_url_id(sid) is not None:
            sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        self._conn.execute(
            "INSERT INTO urls (short_id, original_url, user_id) VALUES (?, ?, ?)",
            (sid, url, user_id),
        )
        self._conn.commit()
        return sid

    def _get_url_id(self, sid: str) -> int | None:
        row = self._conn.execute(
            "SELECT id FROM urls WHERE short_id = ?", (sid,)
        ).fetchone()
        return row["id"] if row else None

    def resolve(self, sid: str) -> str | None:
        url_id = self._get_url_id(sid)
        if url_id is None:
            return None
        row = self._conn.execute(
            "SELECT original_url FROM urls WHERE short_id = ?", (sid,)
        ).fetchone()
        if row is None:
            return None
        self.record_click(sid)
        return row["original_url"]

    def record_click(self, sid: str, referrer: str | None = None) -> ClickRecord:
        url_id = self._get_url_id(sid)
        if url_id is None:
            return ClickRecord(
                timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                referrer=referrer,
            )
        self._conn.execute(
            "INSERT INTO clicks (url_id, referrer) VALUES (?, ?)",
            (url_id, referrer),
        )
        self._conn.commit()
        return ClickRecord(
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            referrer=referrer,
        )

    def get_history(self, sid: str) -> list[ClickRecord]:
        url_id = self._get_url_id(sid)
        if url_id is None:
            return []
        rows = self._conn.execute(
            "SELECT clicked_at, referrer FROM clicks WHERE url_id = ? ORDER BY id",
            (url_id,),
        ).fetchall()
        return [
            ClickRecord(timestamp=r["clicked_at"], referrer=r["referrer"]) for r in rows
        ]

    def stats(self, sid: str) -> int:
        url_id = self._get_url_id(sid)
        if url_id is None:
            return 0
        row = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM clicks WHERE url_id = ?", (url_id,)
        ).fetchone()
        return row["cnt"] if row else 0

    def peek(self, sid: str) -> str | None:
        url_id = self._get_url_id(sid)
        if url_id is None:
            return None
        row = self._conn.execute(
            "SELECT original_url FROM urls WHERE short_id = ?", (sid,)
        ).fetchone()
        return row["original_url"] if row else None

    def get_owner(self, sid: str) -> int | None:
        row = self._conn.execute(
            "SELECT user_id FROM urls WHERE short_id = ?", (sid,)
        ).fetchone()
        return row["user_id"] if row and row["user_id"] else None

    def close(self) -> None:
        self._conn.close()


class SqliteUserRepo(UserRepository):
    def __init__(self, db_path: str = "urlshortener.db") -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        self._conn.commit()

    def create_user(self, email: str, password_hash: str) -> User:
        try:
            cur = self._conn.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash),
            )
            self._conn.commit()
            row = self._conn.execute(
                "SELECT * FROM users WHERE id = ?", (cur.lastrowid,)
            ).fetchone()
            return User(
                id=row["id"],
                email=row["email"],
                password_hash=row["password_hash"],
                created_at=row["created_at"],
            )
        except sqlite3.IntegrityError:
            raise ValueError("Email already registered")

    def get_by_email(self, email: str) -> User | None:
        row = self._conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if row is None:
            return None
        return User(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )

    def get_by_id(self, user_id: int) -> User | None:
        row = self._conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            return None
        return User(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )

    def close(self) -> None:
        self._conn.close()
