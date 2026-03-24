"""
PYQ (Previous Year Questions) routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.pyq import PYQListResponse, CheckAnswerRequest, CheckAnswerResponse
from app.core.dependencies import get_current_user_id

router = APIRouter()


@router.get("/questions", response_model=PYQListResponse)
async def get_questions(
    subject: str,
    class_level: int,
    year: int | None = None,
    chapter: str | None = None,
    difficulty: str | None = None,
    page: int = 1,
    limit: int = 10,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get previous year questions filtered by subject, class, etc.

    TODO (Phase 1): Query Supabase pyq_questions table.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="PYQ not yet implemented — Phase 1",
    )


@router.post("/check-answer", response_model=CheckAnswerResponse)
async def check_answer(
    request: CheckAnswerRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Check a student's answer to a PYQ and provide AI feedback.

    TODO (Phase 1):
    1. Fetch question + answer key from Supabase
    2. Call AI to evaluate and provide feedback
    3. Record attempt in pyq_attempts table
    4. Award XP
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="PYQ answer checking not yet implemented — Phase 1",
    )
