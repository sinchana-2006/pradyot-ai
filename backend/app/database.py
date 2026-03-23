"""
Supabase database connection and utilities.
Loads credentials from environment variables - never hardcoded.
"""

import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env from project root (pradyot-ai/.env) - never hardcode credentials
_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_project_root / ".env")


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client.
    Uses SUPABASE_URL and SUPABASE_ANON_KEY from environment.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError(
            "Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_ANON_KEY in .env"
        )
    
    return create_client(url, key)


# Optional: Initialize client for import elsewhere
# Use get_supabase_client() when you need a fresh connection
supabase: Client | None = None


def init_db():
    """Initialize the Supabase client (call at app startup if needed)."""
    global supabase
    supabase = get_supabase_client()
    return supabase
