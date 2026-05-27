"""
Supabase database connection.
"""

from supabase import create_client, Client
from app.core.config import settings

_service_client: Client | None = None
_anon_client: Client | None = None


def _is_missing_or_placeholder(value: str) -> bool:
    cleaned = (value or "").strip()
    if not cleaned:
        return True
    placeholder_tokens = ("your-", "change-this", "example", "placeholder")
    return any(token in cleaned.lower() for token in placeholder_tokens)


def _validate_config(url: str, key: str, key_name: str) -> None:
    if _is_missing_or_placeholder(url):
        raise RuntimeError(
            "Supabase is not configured: set a valid SUPABASE_URL in backend/.env."
        )
    if _is_missing_or_placeholder(key):
        raise RuntimeError(
            f"Supabase is not configured: set a valid {key_name} in backend/.env."
        )


def get_db() -> Client:
    """Return the Supabase client (service role) for backend DB operations."""
    global _service_client
    if _service_client is None:
        _validate_config(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY,
            "SUPABASE_SERVICE_KEY",
        )
        try:
            _service_client = create_client(
                settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Supabase service client: {exc}") from exc
    return _service_client


def get_auth_client() -> Client:
    """Return the Supabase client (anon key) for Auth operations."""
    global _anon_client
    if _anon_client is None:
        _validate_config(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY, "SUPABASE_ANON_KEY")
        try:
            _anon_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize Supabase auth client: {exc}") from exc
    return _anon_client


def check_db_connection() -> tuple[bool, str]:
    """
    Validate DB connectivity using a lightweight query.
    Returns (True, "ok") on success, else (False, error_message).
    """
    try:
        db = get_db()
        db.table("students").select("id").limit(1).execute()
        return True, "ok"
    except Exception as exc:
        return False, str(exc)
