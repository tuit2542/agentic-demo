from __future__ import annotations

import os
import time
from dataclasses import dataclass


@dataclass
class RateLimitInfo:
    limit: int
    remaining: int
    reset_at: float


class RateLimiter:
    """Simple in-memory sliding window rate limiter."""

    def __init__(self, limit: int = 100, window: int = 60) -> None:
        self._limit = limit
        self._window = window
        self._requests: dict[str, list[float]] = {}

    def check(self, key: str) -> bool:
        """Return True if request is allowed."""
        now = time.time()
        self._cleanup(key, now)

        if key not in self._requests:
            self._requests[key] = []

        if len(self._requests[key]) >= self._limit:
            return False

        self._requests[key].append(now)
        return True

    def info(self, key: str) -> RateLimitInfo:
        """Get current rate limit info for key."""
        now = time.time()
        self._cleanup(key, now)

        requests = self._requests.get(key, [])
        remaining = max(0, self._limit - len(requests))

        if requests:
            reset_at = requests[0] + self._window
        else:
            reset_at = now + self._window

        return RateLimitInfo(
            limit=self._limit,
            remaining=remaining,
            reset_at=reset_at,
        )

    def _cleanup(self, key: str, now: float) -> None:
        """Remove expired entries."""
        if key in self._requests:
            self._requests[key] = [
                t for t in self._requests[key] if now - t < self._window
            ]


def get_rate_limiter() -> RateLimiter:
    """Create rate limiter from env config."""
    limit = int(os.getenv("RATE_LIMIT", "100"))
    window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    return RateLimiter(limit=limit, window=window)
