"""
Google OAuth 2.0 authentication endpoints.

Supports two flows:
  1. Real Google Sign-In: verify an ID token against Google's public certs.
  2. Demo bypass: instant operator login for local dev / hackathon judging.
"""

from datetime import datetime, timezone
from uuid import uuid4

import httpx
from fastapi import APIRouter, HTTPException

from app.models.schemas import AuthResponse, GoogleAuthPayload, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory session store (swap for Redis / DB in production).
_SESSIONS: dict[str, AuthResponse] = {}

GOOGLE_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"


@router.post("/google", response_model=AuthResponse)
async def google_login(payload: GoogleAuthPayload) -> AuthResponse:
    """
    Verify a Google ID token and return a session with role assignment.

    If the token equals the literal string ``demo``, issue a demo commander
    session immediately so the app is fully testable without a real Google
    Cloud Console Client ID.
    """
    # ------------------------------------------------------------------
    # Demo bypass — allows instant login for local testing / hackathon
    # ------------------------------------------------------------------
    if payload.id_token == "demo":
        session = AuthResponse(
            name="Demo Commander",
            email="commander@roadresq.local",
            picture=None,
            role=UserRole.COMMANDER,
            session_token=str(uuid4()),
        )
        _SESSIONS[session.session_token] = session
        return session

    # ------------------------------------------------------------------
    # Real Google token verification
    # ------------------------------------------------------------------
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                GOOGLE_TOKENINFO_URL, params={"id_token": payload.id_token}
            )
            resp.raise_for_status()
            claims = resp.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Token verification failed: {exc}")

    email: str = claims.get("email", "")
    name: str = claims.get("name", email.split("@")[0])
    picture: str | None = claims.get("picture")

    # Simple role mapping — extend with a DB lookup in production.
    role = UserRole.ANALYST
    if email.endswith("@roadresq.local") or "commander" in email.lower():
        role = UserRole.COMMANDER
    elif "logistics" in email.lower() or "supply" in email.lower():
        role = UserRole.LOGISTICS_OFFICER

    session = AuthResponse(
        name=name,
        email=email,
        picture=picture,
        role=role,
        session_token=str(uuid4()),
    )
    _SESSIONS[session.session_token] = session
    return session


@router.get("/me", response_model=AuthResponse | None)
async def current_user(session_token: str = "") -> AuthResponse | None:
    """Return the user profile for a given session token, or None."""
    return _SESSIONS.get(session_token)


@router.post("/demo/{role_name}", response_model=AuthResponse)
async def demo_login(role_name: str) -> AuthResponse:
    """
    Quick demo login for any role (commander, logistics_officer, analyst).
    No Google credentials required.
    """
    try:
        role = UserRole(role_name)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown role '{role_name}'. Use: commander, logistics_officer, analyst",
        )

    titles = {
        UserRole.COMMANDER: "Demo Commander",
        UserRole.LOGISTICS_OFFICER: "Demo Logistics Officer",
        UserRole.ANALYST: "Demo Analyst",
    }

    session = AuthResponse(
        name=titles[role],
        email=f"{role_name}@roadresq.local",
        picture=None,
        role=role,
        session_token=str(uuid4()),
    )
    _SESSIONS[session.session_token] = session
    return session
