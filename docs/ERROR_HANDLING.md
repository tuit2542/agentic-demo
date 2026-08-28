# Error Handling Pattern

> Agentic Demo — Standard error response format

---

## Response Format

All errors follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

This is **FastAPI's default `HTTPException` format**. No custom error wrapper needed.

---

## HTTP Status Codes

| Code | When to Use | Example |
|------|-------------|---------|
| `200` | Success (GET, stats) | `GET /stats/{sid}` |
| `201` | Created (POST) | `POST /shorten` |
| `307` | Redirect | `GET /{sid}` → redirect to URL |
| `404` | Resource not found | Unknown short_id |
| `422` | Validation error | Invalid URL format, missing body |
| `500` | Server error | Unexpected failure |

---

## Error Patterns

### 1. Resource Not Found (404)
```python
from fastapi import HTTPException

if result is None:
    raise HTTPException(
        status_code=404,
        detail="Short URL not found"
    )
```

### 2. Validation Error (422)
FastAPI/Pydantic handles this automatically:
```python
from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    url: HttpUrl  # FastAPI returns 422 if invalid
```

Response when validation fails:
```json
{
  "detail": [
    {
      "type": "url_parsing",
      "loc": ["body", "url"],
      "msg": "Input should be a valid URL, relative URL without a base",
      "input": "not-a-url"
    }
  ]
}
```

### 3. Duplicate Resource (409)
```python
# When implementing unique constraints
if store.exists(url):
    raise HTTPException(
        status_code=409,
        detail="URL already shortened"
    )
```

### 4. Rate Limited (429)
```python
# When implementing rate limiting
raise HTTPException(
    status_code=429,
    detail="Rate limit exceeded. Try again in 60 seconds."
)
```

---

## Rules for Agent

1. **Always use `HTTPException`** — don't return raw dicts for errors
2. **Always include `detail`** — the error message string
3. **Never expose internals** — no stack traces, no DB errors in response
4. **Use correct status codes** — match the HTTP semantics
5. **Test all error paths** — every `raise HTTPException` needs a test

---

## Test Pattern

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_unknown_short_id_returns_404():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found"

@pytest.mark.asyncio
async def test_invalid_url_returns_422():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422
```

---

*Last updated: 2026-08-28*
