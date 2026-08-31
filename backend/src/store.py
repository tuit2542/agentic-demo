from __future__ import annotations

import random
import string
from datetime import datetime, timezone

from src.models import ClickRecord


class UrlStore:
    def __init__(self) -> None:
        self._urls: dict[str, str] = {}
        self._clicks: dict[str, int] = {}
        self._history: dict[str, list[ClickRecord]] = {}

    def shorten(self, url: str) -> str:
        sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        while sid in self._urls:
            sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        self._urls[sid] = url
        self._clicks[sid] = 0
        self._history[sid] = []
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

    def stats(self, sid: str) -> int:
        return self._clicks.get(sid, 0)
