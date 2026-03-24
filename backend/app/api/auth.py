"""
Auth routes — register and login.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user account.

    TODO (Phase 1): Connect to Supabase Auth for actual user creation.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Auth not yet implemented — Phase 1",
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login with email and password.

    TODO (Phase 1): Validate against Supabase Auth.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Auth not yet implemented — Phase 1",
    )
