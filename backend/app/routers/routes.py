"""
Route-planning endpoints. Combines Google Maps directions with active
incident/weather data so the app can suggest hazard-free alternate routes.
"""

from fastapi import APIRouter

from app.models.schemas import RouteRequest, RouteResponse
from app.services.maps import get_routes

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("", response_model=RouteResponse)
async def plan_route(payload: RouteRequest) -> RouteResponse:
    options = await get_routes(payload.origin, payload.destination, payload.avoid_hazards)
    return RouteResponse(origin=payload.origin, destination=payload.destination, routes=options)
