import random
import string


class UrlStore:
    def __init__(self):
        self._urls: dict[str, str] = {}
        self._clicks: dict[str, int] = {}

    def shorten(self, url: str) -> str:
        sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        while sid in self._urls:
            sid = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        self._urls[sid] = url
        self._clicks[sid] = 0
        return sid

    def resolve(self, sid: str) -> str | None:
        if sid in self._urls:
            self._clicks[sid] += 1
            return self._urls[sid]
        return None

    def stats(self, sid: str) -> int:
        return self._clicks.get(sid, 0)
