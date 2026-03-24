"""
Student profile routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.students import StudentProfileRequest, StudentProfileResponse
from app.core.dependencies import get_current_user_id

router = APIRouter()


@router.post("/profile", response_model=StudentProfileResponse)
async def create_or_update_profile(
    request: StudentProfileRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Create or update the student's academic profile.

    TODO (Phase 1): Upsert into Supabase student_profiles table.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Student profile not yet implemented — Phase 1",
    )


@router.get("/profile", response_model=StudentProfileResponse)
async def get_profile(user_id: str = Depends(get_current_user_id)):
    """
    Get the current student's profile.

    TODO (Phase 1): Fetch from Supabase student_profiles table.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Student profile not yet implemented — Phase 1",
    )
