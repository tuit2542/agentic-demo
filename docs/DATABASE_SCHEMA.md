# Database Schema

> Agentic Demo — Current + Future data layer

---

## Current: In-Memory Store

```python
# src/store.py
class UrlStore:
    _urls: dict[str, str]      # short_id → original_url
    _clicks: dict[str, int]    # short_id → click_count
```

**Limitations:**
- Data lost on restart
- No persistence
- Single process only
- No indexing

---

## Future: SQLite Schema

> Implement when migrating from in-memory store.

```sql
-- urls table
CREATE TABLE urls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    short_id    TEXT    NOT NULL UNIQUE,    -- 6-char alphanumeric
    original_url TEXT   NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    expires_at  TEXT    DEFAULT NULL        -- NULL = never expires
);

CREATE INDEX idx_short_id ON urls(short_id);
CREATE INDEX idx_original_url ON urls(original_url);

-- clicks table (for analytics)
CREATE TABLE clicks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url_id      INTEGER NOT NULL REFERENCES urls(id),
    clicked_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    ip_address  TEXT    DEFAULT NULL,
    user_agent  TEXT    DEFAULT NULL
);

CREATE INDEX idx_url_id ON clicks(url_id);
CREATE INDEX idx_clicked_at ON clicks(clicked_at);
```

---

## Entity Relationship

```
urls (1) ──── (many) clicks
  │                  │
  ├── short_id       ├── url_id (FK)
  ├── original_url   ├── clicked_at
  ├── created_at     ├── ip_address
  └── expires_at     └── user_agent
```

---

## Migration Path

| Phase | Store | When |
|-------|-------|------|
| 1 (current) | In-memory `dict` | MVP, demo |
| 2 | SQLite | First deploy |
| 3 | PostgreSQL | Scale / multi-process |

---

## Pydantic Models for DB Layer

```python
from pydantic import BaseModel
from datetime import datetime

class UrlRecord(BaseModel):
    id: int
    short_id: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None = None

class ClickRecord(BaseModel):
    id: int
    url_id: int
    clicked_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None
```

---

## Store Interface (Contract)

When implementing new store backends, implement this interface:

```python
from abc import ABC, abstractmethod

class BaseStore(ABC):
    @abstractmethod
    def shorten(self, url: str) -> str:
        """Create short URL, return short_id."""

    @abstractmethod
    def resolve(self, short_id: str) -> str | None:
        """Resolve short_id to original URL."""

    @abstractmethod
    def stats(self, short_id: str) -> dict:
        """Return stats for a short URL."""
```

---

*Last updated: 2026-08-28*
