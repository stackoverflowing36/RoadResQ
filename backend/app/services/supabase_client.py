"""
Thin wrapper around the Supabase client.

Handles storing/reading incidents and alerts so route/incident handling
logic doesn't need to know about Supabase directly. This makes it easy
to swap the backing store later if needed.
"""

from functools import lru_cache

from supabase import Client, create_client

from app.core.config import get_settings


@lru_cache
def get_supabase() -> Client | None:
    settings = get_settings()
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        # Allows local dev / demo mode without a live Supabase project.
        return None
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


class SupabaseUnavailable(RuntimeError):
    """Raised when a Supabase call is attempted without credentials configured."""
