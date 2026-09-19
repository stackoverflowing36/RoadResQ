"""
Incident reporting endpoints.

Supports the "store-carry-forward" flow: a device can report an incident
it captured while offline (synced_offline=True) and the server just
records the original timestamp instead of "now".
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.schemas import Incident, IncidentCreate
from app.services.supabase_client import get_supabase

router = APIRouter(prefix="/incidents", tags=["incidents"])

# In-memory fallback store used when Supabase isn't configured (demo mode).
_DEMO_INCIDENTS: list[Incident] = []


@router.post("", response_model=Incident, status_code=201)
async def report_incident(payload: IncidentCreate) -> Incident:
    incident = Incident(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        reported_at=payload.reported_at or datetime.now(timezone.utc),
        **payload.model_dump(exclude={"reported_at"}),
    )

    supabase = get_supabase()
    if supabase is None:
        _DEMO_INCIDENTS.append(incident)
        return incident

    result = supabase.table("incidents").insert(incident.model_dump(mode="json")).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to store incident")
    return incident


@router.get("", response_model=list[Incident])
async def list_incidents(
    lat: float | None = None, lng: float | None = None, radius_km: float = 25.0
) -> list[Incident]:
    """
    List recent incidents, optionally filtered to a radius around a point.
    Used by the app's on-device Edge AI / dynamic rerouting logic.
    """
    supabase = get_supabase()
    if supabase is None:
        return _DEMO_INCIDENTS

    result = supabase.table("incidents").select("*").order("created_at", desc=True).limit(200).execute()
    return result.data or []
