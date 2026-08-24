from pydantic import BaseModel, HttpUrl


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_id: str
    short_url: str


class StatsResponse(BaseModel):
    short_id: str
    clicks: int
    original_url: str


class ErrorResponse(BaseModel):
    detail: str
