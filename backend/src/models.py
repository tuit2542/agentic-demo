from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class ClickRecord(BaseModel):
    timestamp: str
    referrer: str | None = None


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_id: str
    short_url: str


class StatsResponse(BaseModel):
    short_id: str
    clicks: int
    original_url: str
    clicks_history: list[ClickRecord]


class ErrorResponse(BaseModel):
    detail: str
