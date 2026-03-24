"""
Progress routes — XP, badges, and study summary.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.progress import ProgressSummaryResponse
from app.core.dependencies import get_current_user_id

router = APIRouter()


@router.get("/summary", response_model=ProgressSummaryResponse)
async def get_progress_summary(user_id: str = Depends(get_current_user_id)):
    """
    Get the student's overall progress summary.

    TODO (Phase 1): Aggregate from Supabase student_progress and badge_awards.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Progress tracking not yet implemented — Phase 1",
    )
