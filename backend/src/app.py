from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config import get_base_url, get_cors_origins
from src.models import ShortenRequest, ShortenResponse, StatsResponse
from src.store import UrlStore


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

    store = UrlStore()

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/shorten", response_model=ShortenResponse, status_code=201)
    async def shorten(req: ShortenRequest) -> ShortenResponse:
        sid = store.shorten(str(req.url))
        base = get_base_url()
        return ShortenResponse(short_id=sid, short_url=f"{base}/{sid}")

    @app.get("/stats/{sid}", response_model=StatsResponse)
    async def stats(sid: str) -> StatsResponse:
        original = store._urls.get(sid)
        if original is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        clicks = store.stats(sid)
        history = store.get_history(sid)
        return StatsResponse(
            short_id=sid, clicks=clicks, original_url=original, clicks_history=history
        )

    @app.get("/{sid}", response_class=RedirectResponse, status_code=307)
    async def redirect_url(sid: str) -> RedirectResponse:
        url = store.resolve(sid)
        if url is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        return RedirectResponse(url=url)

    return app


if __name__ == "__main__":
    import uvicorn

    from src.config import get_host, get_port

    uvicorn.run(create_app(), host=get_host(), port=get_port())
