from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from src.models import ShortenRequest, ShortenResponse, StatsResponse
from src.store import UrlStore


def create_app() -> FastAPI:
    app = FastAPI(title="URL Shortener")
    store = UrlStore()

    @app.post("/shorten", response_model=ShortenResponse, status_code=201)
    async def shorten(req: ShortenRequest) -> ShortenResponse:
        sid = store.shorten(str(req.url))
        return ShortenResponse(short_id=sid, short_url=f"http://localhost/{sid}")

    @app.get("/stats/{sid}", response_model=StatsResponse)
    async def stats(sid: str) -> StatsResponse:
        original = store._urls.get(sid)
        if original is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        clicks = store.stats(sid)
        return StatsResponse(short_id=sid, clicks=clicks, original_url=original)

    @app.get("/{sid}", response_class=RedirectResponse, status_code=307)
    async def redirect_url(sid: str) -> RedirectResponse:
        url = store.resolve(sid)
        if url is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        return RedirectResponse(url=url)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
