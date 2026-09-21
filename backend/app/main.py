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

# --- Static file mounts for segregated desktop & mobile apps ----------------
_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
_DESKTOP_DIR = _ROOT_DIR / "desktop-web"
_MOBILE_DIR = _ROOT_DIR / "mobile-web"
_FRONTEND_WEB_DIR = _ROOT_DIR / "frontend-web"

if _DESKTOP_DIR.is_dir():
    app.mount("/desktop", StaticFiles(directory=str(_DESKTOP_DIR), html=True), name="desktop")
    app.mount("/control-room", StaticFiles(directory=str(_DESKTOP_DIR), html=True), name="control-room")
elif _FRONTEND_WEB_DIR.is_dir():
    app.mount("/control-room", StaticFiles(directory=str(_FRONTEND_WEB_DIR), html=True), name="control-room")

if _MOBILE_DIR.is_dir():
    app.mount("/mobile", StaticFiles(directory=str(_MOBILE_DIR), html=True), name="mobile")


@app.get("/")
async def root():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/health")
async def health():
    return {"status": "healthy"}
