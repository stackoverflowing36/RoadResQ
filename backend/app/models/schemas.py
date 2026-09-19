"""
Pydantic models shared across the API.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class IncidentType(str, Enum):
    LANDSLIDE = "landslide"
    FLOOD = "flood"
    ROAD_BLOCK = "road_block"
    ACCIDENT = "accident"
    WEATHER_HAZARD = "weather_hazard"
    OTHER = "other"


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentCreate(BaseModel):
    reporter_id: Optional[str] = Field(None, description="Device / user id of reporter")
    incident_type: IncidentType
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    latitude: float
    longitude: float
    description: Optional[str] = None
    photo_url: Optional[str] = None
    reported_at: Optional[datetime] = None
    synced_offline: bool = Field(
        False, description="True if this record was captured offline and is now syncing"
    )


class Incident(IncidentCreate):
    id: str
    created_at: datetime
    verified: bool = False


class AlertOut(BaseModel):
    id: str
    title: str
    message: str
    severity: IncidentSeverity
    latitude: float
    longitude: float
    radius_km: float = 10.0
    created_at: datetime


class RoutePoint(BaseModel):
    latitude: float
    longitude: float


class RouteRequest(BaseModel):
    origin: RoutePoint
    destination: RoutePoint
    avoid_hazards: bool = True


class RouteOption(BaseModel):
    summary: str
    distance_km: float
    duration_minutes: float
    is_alternate: bool = False
    hazard_free: bool = True
    polyline: Optional[str] = Field(
        None, description="Encoded polyline for map rendering"
    )


class RouteResponse(BaseModel):
    origin: RoutePoint
    destination: RoutePoint
    routes: list[RouteOption]


class WeatherAlert(BaseModel):
    latitude: float
    longitude: float
    condition: str
    risk_level: IncidentSeverity
    description: str
    valid_until: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Authentication & RBAC
# ---------------------------------------------------------------------------


class UserRole(str, Enum):
    COMMANDER = "commander"
    LOGISTICS_OFFICER = "logistics_officer"
    ANALYST = "analyst"


class GoogleAuthPayload(BaseModel):
    """Payload sent by the frontend after Google Sign-In."""

    id_token: str = Field(..., description="Google ID token (JWT credential)")


class AuthResponse(BaseModel):
    """Returned to the frontend after successful authentication."""

    name: str
    email: str
    picture: Optional[str] = None
    role: UserRole = UserRole.ANALYST
    session_token: str = Field(..., description="Server-issued session token")


# ---------------------------------------------------------------------------
# Logistics — Supply Convoy & Corridor Tracking
# ---------------------------------------------------------------------------


class ConvoyStatus(str, Enum):
    ON_ROUTE = "on_route"
    DELAYED = "delayed"
    DIVERTED = "diverted"
    HALTED = "halted"
    DELIVERED = "delivered"


class SupplyConvoy(BaseModel):
    id: str
    call_sign: str = Field(..., description="e.g. MEDEVAC-03, FUEL-NH6-12")
    cargo_type: str = Field(..., description="Medical, Fuel, Rations, Earthmover, etc.")
    status: ConvoyStatus = ConvoyStatus.ON_ROUTE
    origin: str
    destination: str
    current_latitude: float
    current_longitude: float
    eta_minutes: float
    delay_hours: float = 0.0
    corridor: str = Field("NH-6", description="Highway corridor identifier")
    last_updated: datetime


class CorridorStatus(BaseModel):
    corridor_id: str = Field(..., description="e.g. NH-6, NH-10, NH-58")
    name: str
    status: str = Field("open", description="open | partial_block | total_block")
    active_incidents: int = 0
    delay_index_hours: float = 0.0
    detour_available: bool = True
    detour_summary: Optional[str] = None
    last_updated: datetime


class SitrepReport(BaseModel):
    """Logistics Situation Report (SITREP) for disaster management authorities."""

    report_id: str
    generated_at: datetime
    corridor_id: str
    summary: str
    active_incidents: int
    convoys_affected: int
    total_delay_hours: float
    roads_blocked: int
    roads_partial: int
    roads_open: int
    recommendations: list[str] = []
