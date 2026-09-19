"""
Routing service backed by the Google Maps Directions API.

Falls back to a straight-line demo route if no API key is configured,
so the rest of the app is runnable without billing set up.
"""

import math

import httpx

from app.core.config import get_settings
from app.models.schemas import RouteOption, RoutePoint

DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


def _haversine_km(a: RoutePoint, b: RoutePoint) -> float:
    r = 6371.0
    lat1, lat2 = math.radians(a.latitude), math.radians(b.latitude)
    dlat = math.radians(b.latitude - a.latitude)
    dlon = math.radians(b.longitude - a.longitude)
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(h))


def _demo_route(origin: RoutePoint, destination: RoutePoint) -> list[RouteOption]:
    distance = _haversine_km(origin, destination)
    return [
        RouteOption(
            summary="Direct route (demo mode, no Maps API key set)",
            distance_km=round(distance, 1),
            duration_minutes=round(distance / 40 * 60, 0),  # assume 40 km/h avg
            is_alternate=False,
            hazard_free=True,
        )
    ]


async def get_routes(
    origin: RoutePoint, destination: RoutePoint, avoid_hazards: bool = True
) -> list[RouteOption]:
    settings = get_settings()
    if not settings.GOOGLE_MAPS_API_KEY:
        return _demo_route(origin, destination)

    params = {
        "origin": f"{origin.latitude},{origin.longitude}",
        "destination": f"{destination.latitude},{destination.longitude}",
        "alternatives": "true",
        "key": settings.GOOGLE_MAPS_API_KEY,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(DIRECTIONS_URL, params=params)
        response.raise_for_status()
        data = response.json()

    routes: list[RouteOption] = []
    for i, route in enumerate(data.get("routes", [])):
        leg = route["legs"][0]
        routes.append(
            RouteOption(
                summary=route.get("summary", f"Route {i + 1}"),
                distance_km=round(leg["distance"]["value"] / 1000, 1),
                duration_minutes=round(leg["duration"]["value"] / 60, 0),
                is_alternate=i > 0,
                hazard_free=True,  # refined later against active incident data
                polyline=route.get("overview_polyline", {}).get("points"),
            )
        )
    return routes or _demo_route(origin, destination)
