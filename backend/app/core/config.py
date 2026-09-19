"""
Application configuration.
Loads settings from environment variables (see .env.example).
"""

import os
from functools import lru_cache


class Settings:
    APP_NAME: str = "RoadResQ API"
    API_V1_PREFIX: str = "/api/v1"

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Weather (Open-Meteo needs no API key, but keep a slot for future providers)
    OPEN_METEO_BASE_URL: str = os.getenv(
        "OPEN_METEO_BASE_URL", "https://api.open-meteo.com/v1/forecast"
    )

    # Google Maps
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # CORS
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()
