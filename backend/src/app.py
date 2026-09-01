from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from src.auth import (
    create_token,
    get_current_user,
    get_user_repo,
    hash_password,
    verify_password,
)
from src.config import get_base_url, get_cors_origins, get_database_url
from src.models import (
    LoginRequest,
    RegisterRequest,
    ShortenRequest,
    ShortenResponse,
    StatsResponse,
    TokenResponse,
    UserResponse,
)
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
    user_repo = get_user_repo()

    def _rate_limit_headers(key: str) -> dict[str, str]:
        info = limiter.info(key)
        return {
            "X-RateLimit-Limit": str(info.limit),
            "X-RateLimit-Remaining": str(info.remaining),
            "X-RateLimit-Reset": str(int(info.reset_at)),
        }

    # ── Health ──────────────────────────────────────────
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    # ── Auth ────────────────────────────────────────────
    @app.post("/auth/register", response_model=UserResponse, status_code=201)
    async def register(req: RegisterRequest) -> UserResponse:
        if user_repo.get_by_email(req.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        hashed = hash_password(req.password)
        user = user_repo.create_user(req.email, hashed)
        return UserResponse(id=user.id, email=user.email, created_at=user.created_at)

    @app.post("/auth/login", response_model=TokenResponse)
    async def login(req: LoginRequest) -> TokenResponse:
        user = user_repo.get_by_email(req.email)
        if user is None or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_token(user.id, user.email)
        return TokenResponse(access_token=token)

    @app.get("/auth/me", response_model=UserResponse)
    async def me(user: dict = Depends(get_current_user)) -> UserResponse:
        user_obj = user_repo.get_by_id(int(user["sub"]))
        if user_obj is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(
            id=user_obj.id, email=user_obj.email, created_at=user_obj.created_at
        )

    # ── URL Shortener (authenticated) ───────────────────
    @app.post("/shorten", response_model=ShortenResponse, status_code=201)
    async def shorten(
        req: ShortenRequest,
        request: Request,
        user: dict = Depends(get_current_user),
    ) -> JSONResponse:
        key = f"shorten:{request.client.host if request.client else 'unknown'}"
        if not limiter.check(key):
            headers = _rate_limit_headers(key)
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again in 60 seconds."},
                headers=headers,
            )
        user_id = int(user["sub"])
        try:
            sid = store.shorten(str(req.url), user_id=user_id, custom_id=req.custom_id)
        except ValueError as e:
            if "already taken" in str(e):
                raise HTTPException(status_code=409, detail=str(e))
            raise
        base = get_base_url()
        headers = _rate_limit_headers(key)
        return JSONResponse(
            status_code=201,
            content=ShortenResponse(
                short_id=sid, short_url=f"{base}/{sid}"
            ).model_dump(),
            headers=headers,
        )

    # ── URL Shortener (anonymous — backward compatible) ─
    @app.post("/shorten-anon", response_model=ShortenResponse, status_code=201)
    async def shorten_anon(req: ShortenRequest, request: Request) -> JSONResponse:
        key = f"shorten:{request.client.host if request.client else 'unknown'}"
        if not limiter.check(key):
            headers = _rate_limit_headers(key)
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again in 60 seconds."},
                headers=headers,
            )
        try:
            sid = store.shorten(str(req.url), custom_id=req.custom_id)
        except ValueError as e:
            if "already taken" in str(e):
                raise HTTPException(status_code=409, detail=str(e))
            raise
        base = get_base_url()
        headers = _rate_limit_headers(key)
        return JSONResponse(
            status_code=201,
            content=ShortenResponse(
                short_id=sid, short_url=f"{base}/{sid}"
            ).model_dump(),
            headers=headers,
        )

    # ── Stats & Redirect ────────────────────────────────
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
