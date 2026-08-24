import pytest
from pydantic import ValidationError
from src.models import ShortenRequest, ShortenResponse, StatsResponse


def test_shorten_request_validates_url():
    req = ShortenRequest(url="https://example.com")
    assert str(req.url) == "https://example.com/"


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


def test_stats_response_fields():
    resp = StatsResponse(
        short_id="abc123", clicks=5, original_url="https://example.com"
    )
    assert resp.clicks == 5
    assert resp.original_url == "https://example.com"
