"""
Supabase database connection.
"""

from supabase import create_client, Client
from app.core.config import settings

_service_client: Client | None = None
_anon_client: Client | None = None


def get_db() -> Client:
    """Return the Supabase client (service role) for backend DB operations."""
    global _service_client
    if _service_client is None:
        _service_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _service_client


def get_auth_client() -> Client:
    """Return the Supabase client (anon key) for Auth operations."""
    global _anon_client
    if _anon_client is None:
        _anon_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    return _anon_client
