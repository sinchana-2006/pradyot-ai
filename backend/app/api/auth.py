"""
Auth routes — register and login.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.auth import (
    RegisterRequest,
    LoginRequest,
    OAuthExchangeRequest,
    TokenResponse,
)
from app.core.security import create_access_token
from app.db.database import get_auth_client

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user account via Supabase Auth.
    Returns a signed JWT that the client should store and send as Bearer token.
    """
    client = get_auth_client()
    try:
        response = client.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
                "options": {"data": {"full_name": request.full_name}},
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {exc}",
        )

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed — check email/password requirements.",
        )

    token = create_access_token({"sub": str(response.user.id), "email": response.user.email})
    return TokenResponse(access_token=token, user_id=str(response.user.id))


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login with email and password via Supabase Auth.
    Returns a signed JWT that the client should store and send as Bearer token.
    """
    client = get_auth_client()
    try:
        response = client.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {exc}",
        )

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token({"sub": str(response.user.id), "email": response.user.email})
    return TokenResponse(access_token=token, user_id=str(response.user.id))


@router.post("/google/exchange", response_model=TokenResponse)
async def exchange_google_token(request: OAuthExchangeRequest):
    """
    Exchange a Supabase OAuth access token for the app JWT.

    Frontend signs in with Google using Supabase JS, then sends Supabase access_token
    here so the backend can verify user identity and issue the app bearer token.
    """
    client = get_auth_client()
    try:
        user_response = client.auth.get_user(request.access_token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Google token verification failed: {exc}",
        )

    user = getattr(user_response, "user", None)
    if user is None or not getattr(user, "id", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google OAuth token.",
        )

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token, user_id=str(user.id))
