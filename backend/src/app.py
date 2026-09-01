from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from src.config import get_base_url, get_cors_origins, get_database_url
from src.models import ShortenRequest, ShortenResponse, StatsResponse
from src.rate_limiter import get_rate_limiter


def _create_store():
    """Create store based on DATABASE_URL env."""
    db_url = get_database_url()
    if db_url:
        from src.store_sqlite import SqliteStore

        return SqliteStore(db_url)
    from src.store import UrlStore

    return UrlStore()


def create_app() -> FastAPI:
    app = FastAPI(
        title="URL Shortener",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS — from env
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    store = _create_store()
    limiter = get_rate_limiter()

    def _rate_limit_headers(key: str) -> dict[str, str]:
        info = limiter.info(key)
        return {
            "X-RateLimit-Limit": str(info.limit),
            "X-RateLimit-Remaining": str(info.remaining),
            "X-RateLimit-Reset": str(int(info.reset_at)),
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/shorten", response_model=ShortenResponse, status_code=201)
    async def shorten(req: ShortenRequest, request: Request) -> JSONResponse:
        key = f"shorten:{request.client.host if request.client else 'unknown'}"
        if not limiter.check(key):
            headers = _rate_limit_headers(key)
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again in 60 seconds."},
                headers=headers,
            )
        sid = store.shorten(str(req.url))
        base = get_base_url()
        headers = _rate_limit_headers(key)
        return JSONResponse(
            status_code=201,
            content=ShortenResponse(
                short_id=sid, short_url=f"{base}/{sid}"
            ).model_dump(),
            headers=headers,
        )

    @app.get("/stats/{sid}", response_model=StatsResponse)
    async def stats(sid: str) -> StatsResponse:
        original = store.peek(sid)
        if original is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        clicks = store.stats(sid)
        history = store.get_history(sid)
        return StatsResponse(
            short_id=sid, clicks=clicks, original_url=original, clicks_history=history
        )

    @app.get("/{sid}", response_class=RedirectResponse, status_code=307)
    async def redirect_url(sid: str, request: Request):
        key = f"redirect:{request.client.host if request.client else 'unknown'}"
        if not limiter.check(key):
            headers = _rate_limit_headers(key)
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again in 60 seconds."},
                headers=headers,
            )
        url = store.resolve(sid)
        if url is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        # Add rate limit headers to redirect response
        headers = _rate_limit_headers(key)
        response = RedirectResponse(url=url, status_code=307)
        for k, v in headers.items():
            response.headers[k] = v
        return response

    return app


if __name__ == "__main__":
    import uvicorn

    from src.config import get_host, get_port

    uvicorn.run(create_app(), host=get_host(), port=get_port())
