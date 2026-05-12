import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse

from tikscraper import TikNinjaUserClient, TikNinjaVideoClient, scrape_analytics_cdp
from api.models import (
    UserResponse,
    VideoResponse,
    MultiUserVideoResponse,
    AnalyticsResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.user_client = TikNinjaUserClient()
    app.state.video_client = TikNinjaVideoClient()
    yield


app = FastAPI(
    title="TikScraper API",
    description="REST API untuk scraping data TikTok via tik.ninja",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
async def root():
    """Redirect ke dokumentasi API."""
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"status": "no favicon"}


# ── Endpoints ────────────────────────────────────────────────────

@app.get("/api/user/{username}", response_model=UserResponse)
async def get_user(username: str):
    """Ambil profil user berdasarkan username."""
    client: TikNinjaUserClient = app.state.user_client
    result = await client.get_user(username)

    if result.success:
        return UserResponse(success=True, data=result.data.to_dict())
    return UserResponse(success=False, error=result.error)


@app.get("/api/users", response_model=dict)
async def get_users(usernames: str = Query(..., description="Comma-separated usernames")):
    """Ambil banyak user secara bersamaan."""
    client: TikNinjaUserClient = app.state.user_client
    user_list = [u.strip() for u in usernames.split(",") if u.strip()]

    if not user_list:
        raise HTTPException(status_code=400, detail="Parameter 'usernames' tidak boleh kosong")

    results = await client.get_users(user_list)

    data = {}
    for username, result in zip(user_list, results):
        if result.success:
            data[username] = result.data.to_dict()
        else:
            data[username] = {"error": result.error}

    return {"success": True, "data": data}


@app.get("/api/videos/{username}", response_model=VideoResponse)
async def get_videos(
    username: str,
    limit: int = Query(20, ge=1, le=500),
    page_size: int = Query(20, ge=1, le=50),
):
    """Ambil video user berdasarkan username."""
    client: TikNinjaVideoClient = app.state.video_client
    videos = await client.get_all_posts(unique_id=username, limit=limit, page_size=page_size)

    if videos:
        return VideoResponse(success=True, data=[v.to_dict() for v in videos])
    return VideoResponse(success=False, error="Tidak ada video ditemukan")


@app.get("/api/videos/multi", response_model=MultiUserVideoResponse)
async def get_videos_multi(
    usernames: str = Query(..., description="Comma-separated usernames"),
    limit: int = Query(20, ge=1, le=500),
    page_size: int = Query(20, ge=1, le=50),
):
    """Ambil video banyak user secara bersamaan."""
    client: TikNinjaVideoClient = app.state.video_client
    user_list = [u.strip() for u in usernames.split(",") if u.strip()]

    if not user_list:
        raise HTTPException(status_code=400, detail="Parameter 'usernames' tidak boleh kosong")

    results = await client.get_all_posts_multi(user_list, limit=limit, page_size=page_size)

    data = {username: [v.to_dict() for v in vids] for username, vids in results.items()}
    return MultiUserVideoResponse(success=True, data=data)


@app.get("/api/analytics/{username}", response_model=AnalyticsResponse)
async def get_analytics(username: str):
    """Ambil analitik akun user beserta info channel (membutuhkan SeleniumBase)."""
    try:
        user_client: TikNinjaUserClient = app.state.user_client
        user_result = await user_client.get_user(username)

        if not user_result.success:
            return AnalyticsResponse(success=False, error=user_result.error)

        analytics = await scrape_analytics_cdp(username)
        analytics["Channel"] = user_result.data.to_dict()

        return AnalyticsResponse(success=True, data=analytics)
    except Exception as e:
        return AnalyticsResponse(success=False, error=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
