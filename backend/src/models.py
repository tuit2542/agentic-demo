from __future__ import annotations

import re

from pydantic import BaseModel, field_validator


class ClickRecord(BaseModel):
    timestamp: str
    referrer: str | None = None


class ShortenRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL is required")
        if not re.match(r"^https?://", v):
            raise ValueError("URL must start with http:// or https://")
        return v


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
