"""
Auth routes — register and login.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import create_access_token
from app.db.database import get_db

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user account via Supabase Auth and issue API JWT.
    """
    try:
        db = get_db()
        result = db.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
                "options": {"data": {"full_name": request.full_name}},
            }
        )
        user = getattr(result, "user", None)
        if not user or not getattr(user, "id", None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed",
            )
        access_token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=access_token, user_id=str(user.id))
    except HTTPException:
        raise
    except Exception as exc:
        message = str(exc).lower()
        if "already" in message or "exists" in message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service unavailable",
        ) from exc


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login with email and password via Supabase Auth and issue API JWT.
    """
    try:
        db = get_db()
        result = db.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
        user = getattr(result, "user", None)
        if not user or not getattr(user, "id", None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        access_token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=access_token, user_id=str(user.id))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from exc
