"""
Alert distribution endpoints — pushed to nearby travelers and field teams.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

from app.models.schemas import AlertOut, IncidentSeverity, WeatherAlert
from app.services.supabase_client import get_supabase
from app.services.weather import get_weather_risk

router = APIRouter(prefix="/alerts", tags=["alerts"])

_DEMO_ALERTS: list[AlertOut] = []


@router.get("", response_model=list[AlertOut])
async def list_alerts(lat: float, lng: float, radius_km: float = 25.0) -> list[AlertOut]:
    supabase = get_supabase()
    if supabase is None:
        return _DEMO_ALERTS

    result = (
        supabase.table("alerts")
        .select("*")
        .order("created_at", desc=True)
        .limit(100)
        .execute()
    )
    return result.data or []


@router.get("/weather", response_model=WeatherAlert | None)
async def weather_alert(lat: float, lng: float) -> WeatherAlert | None:
    """On-demand hazard check used before starting navigation."""
    return await get_weather_risk(lat, lng)


@router.post("", response_model=AlertOut, status_code=201)
async def create_alert(
    title: str, message: str, severity: IncidentSeverity, lat: float, lng: float
) -> AlertOut:
    """Manually broadcast an alert (e.g. from a verified field report)."""
    alert = AlertOut(
        id=str(uuid4()),
        title=title,
        message=message,
        severity=severity,
        latitude=lat,
        longitude=lng,
        created_at=datetime.now(timezone.utc),
    )

    supabase = get_supabase()
    if supabase is None:
        _DEMO_ALERTS.append(alert)
        return alert

    supabase.table("alerts").insert(alert.model_dump(mode="json")).execute()
    return alert
