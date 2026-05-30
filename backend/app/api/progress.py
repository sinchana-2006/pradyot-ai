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
    Get the student's overall progress summary.
    """
    try:
        db = get_db()
        profile_res = (
            db.table("student_profiles")
            .select("id,full_name")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
        profile = profile_res.data
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found",
            )

        progress_res = (
            db.table("student_progress")
            .select("*")
            .eq("student_id", profile["id"])
            .maybe_single()
            .execute()
        )
        progress = progress_res.data or {}
        badges_res = (
            db.table("badge_awards")
            .select("badge_id")
            .eq("student_id", profile["id"])
            .execute()
        )
        badges = [row["badge_id"] for row in (badges_res.data or [])]
        return ProgressSummaryResponse(
            student_name=profile["full_name"],
            xp_total=progress.get("xp_total", 0),
            xp_this_week=progress.get("xp_this_week", 0),
            study_streak_days=progress.get("study_streak_days", 0),
            badges=badges,
            subjects_covered=progress.get("subject_stats", {}),
            weak_topics=progress.get("weak_topics", []),
            strong_topics=progress.get("strong_topics", []),
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch progress summary",
        ) from exc
