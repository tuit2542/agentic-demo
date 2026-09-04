from __future__ import annotations

import re

from pydantic import BaseModel, field_validator

RESERVED_IDS = {"health", "stats", "docs", "redoc", "auth", "shorten", "shorten-anon"}
MAX_TTL = 31_536_000  # 1 year in seconds


class ClickRecord(BaseModel):
    timestamp: str
    referrer: str | None = None


class ShortenRequest(BaseModel):
    url: str
    custom_id: str | None = None
    expires_in: int | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL is required")
        if not re.match(r"^https?://", v):
            raise ValueError("URL must start with http:// or https://")
        return v

    @field_validator("custom_id")
    @classmethod
    def validate_custom_id(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if len(v) < 3 or len(v) > 20:
            raise ValueError("Custom ID must be 3-20 characters")
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Custom ID can only contain letters, numbers, hyphens, underscores"
            )
        if v.lower() in RESERVED_IDS:
            raise ValueError(f"'{v}' is a reserved path")
        return v

    @field_validator("expires_in")
    @classmethod
    def validate_expires_in(cls, v: int | None) -> int | None:
        if v is None:
            return None
        if v < 1 or v > MAX_TTL:
            raise ValueError("expires_in must be between 1 and 31536000 seconds")
        return v


class ShortenResponse(BaseModel):
    short_id: str
    short_url: str
    expires_at: str | None = None


class StatsResponse(BaseModel):
    short_id: str
    clicks: int
    original_url: str
    clicks_history: list[ClickRecord]
    expired: bool = False
    expires_at: str | None = None


class ReferrerStat(BaseModel):
    referrer: str | None
    count: int


class AnalyticsResponse(BaseModel):
    short_id: str
    total_clicks: int
    unique_referrers: int
    top_referrers: list[ReferrerStat]
    clicks_by_hour: dict[str, int]
    recent_clicks: list[ClickRecord]
    expired: bool = False
    expires_at: str | None = None


class ErrorResponse(BaseModel):
    detail: str


class RegisterRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Email is required")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: str
