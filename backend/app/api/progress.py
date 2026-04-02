"""
Progress routes — XP, badges, and study summary.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.progress import ProgressSummaryResponse
from app.core.dependencies import get_current_user_id
from app.db.database import get_db

router = APIRouter()


@router.get("/summary", response_model=ProgressSummaryResponse)
async def get_progress_summary(user_id: str = Depends(get_current_user_id)):
    """
    Get the student's overall progress summary, including XP, streak, badges,
    subject stats, and weak/strong topics.
    """
    db = get_db()

    # Fetch profile
    try:
        profile_result = (
            db.table("student_profiles")
            .select("id, full_name")
            .eq("user_id", user_id)
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch profile: {exc}",
        )

    profile_rows = profile_result.data or []
    if not profile_rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found. Please complete onboarding first.",
        )
    profile = profile_rows[0]

    # Fetch progress
    progress = {
        "xp_total": 0,
        "xp_this_week": 0,
        "study_streak_days": 0,
        "subject_stats": {},
        "weak_topics": [],
        "strong_topics": [],
    }
    try:
        prog_result = (
            db.table("student_progress")
            .select("*")
            .eq("student_id", profile["id"])
            .execute()
        )
        prog_rows = prog_result.data or []
        if prog_rows:
            progress.update(prog_rows[0])
    except Exception:
        pass

    # Fetch badges
    badges: list[str] = []
    try:
        badge_result = (
            db.table("badge_awards")
            .select("badge_id")
            .eq("student_id", profile["id"])
            .execute()
        )
        badges = [b["badge_id"] for b in (badge_result.data or [])]
    except Exception:
        pass

    return ProgressSummaryResponse(
        student_name=profile["full_name"],
        xp_total=progress.get("xp_total") or 0,
        xp_this_week=progress.get("xp_this_week") or 0,
        study_streak_days=progress.get("study_streak_days") or 0,
        badges=badges,
        subjects_covered=progress.get("subject_stats") or {},
        weak_topics=progress.get("weak_topics") or [],
        strong_topics=progress.get("strong_topics") or [],
    )
