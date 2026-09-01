from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.models import ClickRecord, ShortenRequest, ShortenResponse, StatsResponse


def test_shorten_request_validates_url():
    req = ShortenRequest(url="https://example.com")
    assert req.url == "https://example.com"


def test_shorten_request_rejects_empty_url():
    with pytest.raises(ValidationError):
        ShortenRequest(url="")


def test_shorten_request_rejects_no_url():
    with pytest.raises(ValidationError):
        ShortenRequest()


def test_shorten_response_fields():
    resp = ShortenResponse(short_id="abc123", short_url="http://localhost/abc123")
    assert resp.short_id == "abc123"
    assert resp.short_url == "http://localhost/abc123"


def test_click_record_fields():
    rec = ClickRecord(timestamp="2026-08-31T10:00:00Z")
    assert rec.timestamp == "2026-08-31T10:00:00Z"
    assert rec.referrer is None

    rec_ref = ClickRecord(
        timestamp="2026-08-31T10:00:00Z", referrer="https://google.com"
    )
    assert rec_ref.referrer == "https://google.com"


def test_stats_response_fields():
    rec = ClickRecord(timestamp="2026-08-31T10:00:00Z")
    resp = StatsResponse(
        short_id="abc123",
        clicks=5,
        original_url="https://example.com",
        clicks_history=[rec],
    )
    assert resp.clicks == 5
    assert resp.original_url == "https://example.com"
    assert len(resp.clicks_history) == 1
    assert resp.clicks_history[0].timestamp == "2026-08-31T10:00:00Z"


# === Edge Cases ===


def test_shorten_request_rejects_invalid_url():
    with pytest.raises(ValidationError):
        ShortenRequest(url="not-a-url")


def test_shorten_request_rejects_ftp_url():
    with pytest.raises(ValidationError):
        ShortenRequest(url="ftp://example.com/file.txt")


def test_shorten_request_rejects_missing_scheme():
    with pytest.raises(ValidationError):
        ShortenRequest(url="example.com")


def test_shorten_response_all_fields_required():
    with pytest.raises(ValidationError):
        ShortenResponse(short_id="abc123")


def test_click_record_requires_timestamp():
    with pytest.raises(ValidationError):
        ClickRecord()


def test_stats_response_requires_all_fields():
    with pytest.raises(ValidationError):
        StatsResponse(short_id="abc123", clicks=5)
