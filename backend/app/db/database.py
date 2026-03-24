"""
Supabase database connection.
"""

from supabase import create_client, Client
from app.core.config import settings

_client: Client | None = None


def get_db() -> Client:
    """Return the Supabase client (service role for backend operations)."""
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _client
