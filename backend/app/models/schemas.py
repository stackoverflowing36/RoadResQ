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
