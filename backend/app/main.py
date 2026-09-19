"""
RoadResQ backend entrypoint.

Run locally with:
    uvicorn app.main:app --reload
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers import alerts, auth, incidents, logistics, routes

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered road risk prediction & emergency detection backend.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API routers -----------------------------------------------------------
app.include_router(incidents.router, prefix=settings.API_V1_PREFIX)
app.include_router(alerts.router, prefix=settings.API_V1_PREFIX)
app.include_router(routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(logistics.router, prefix=settings.API_V1_PREFIX)

# --- Static file mount for frontend-web ------------------------------------
# Resolves the frontend-web directory relative to the project root so the
# EOC dashboard is served at /control-room/index.html automatically.
_FRONTEND_WEB_DIR = Path(__file__).resolve().parent.parent.parent / "frontend-web"
if _FRONTEND_WEB_DIR.is_dir():
    app.mount(
        "/control-room",
        StaticFiles(directory=str(_FRONTEND_WEB_DIR), html=True),
        name="control-room",
    )


@app.get("/")
async def root():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/health")
async def health():
    return {"status": "healthy"}
