"""
Weather risk service built on the free Open-Meteo API (no key required).

Used to flag hazardous conditions (heavy rain, storms) along a route or
around a reported incident, feeding into the risk-prediction layer.
"""

import httpx

from app.core.config import get_settings
from app.models.schemas import IncidentSeverity, WeatherAlert

# Open-Meteo weather codes that we treat as hazardous for road travel.
HAZARD_CODES = {
    61: ("Moderate rain", IncidentSeverity.MEDIUM),
    63: ("Heavy rain", IncidentSeverity.HIGH),
    65: ("Violent rain", IncidentSeverity.CRITICAL),
    80: ("Rain showers", IncidentSeverity.MEDIUM),
    82: ("Violent rain showers", IncidentSeverity.CRITICAL),
    95: ("Thunderstorm", IncidentSeverity.HIGH),
    96: ("Thunderstorm with hail", IncidentSeverity.CRITICAL),
    99: ("Severe thunderstorm with hail", IncidentSeverity.CRITICAL),
}


async def get_weather_risk(latitude: float, longitude: float) -> WeatherAlert | None:
    """Fetch current weather for a point and return a WeatherAlert if hazardous."""
    settings = get_settings()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "weather_code,precipitation",
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(settings.OPEN_METEO_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    code = data.get("current", {}).get("weather_code")
    if code in HAZARD_CODES:
        description, risk = HAZARD_CODES[code]
        return WeatherAlert(
            latitude=latitude,
            longitude=longitude,
            condition=description,
            risk_level=risk,
            description=f"{description} detected near this location.",
        )
    return None
