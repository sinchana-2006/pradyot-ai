"""
Student profile routes.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.students import StudentProfileRequest, StudentProfileResponse
from app.core.dependencies import get_current_user_id
from app.db.database import get_db

router = APIRouter()


@router.post("/profile", response_model=StudentProfileResponse)
async def create_or_update_profile(
    request: StudentProfileRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Create or update the student's academic profile.
    Also initialises a student_progress row if one doesn't exist yet.
    """
    db = get_db()

    profile_data = {
        "user_id": user_id,
        "full_name": request.full_name,
        "class_level": request.class_level,
        "board": request.board,
        "preferred_language": request.preferred_language,
        "subjects": request.subjects,
        "state": request.state,
        "updated_at": datetime.utcnow().isoformat(),
    }

    try:
        result = (
            db.table("student_profiles")
            .upsert(profile_data, on_conflict="user_id")
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save profile: {exc}",
        )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile upsert returned no data.",
        )

    row = result.data[0]

    # Ensure a student_progress row exists for this profile
    try:
        db.table("student_progress").upsert(
            {"student_id": row["id"]}, on_conflict="student_id"
        ).execute()
    except Exception:
        pass  # Non-critical — progress row will be created on first chat

    return StudentProfileResponse(
        profile_id=row["id"],
        full_name=row["full_name"],
        class_level=row["class_level"],
        board=row["board"],
        preferred_language=row["preferred_language"],
        subjects=row.get("subjects") or [],
        xp_total=0,
        badges=[],
        created_at=row["created_at"],
    )


@router.get("/profile", response_model=StudentProfileResponse)
async def get_profile(user_id: str = Depends(get_current_user_id)):
    """
    Get the current student's profile along with their total XP.
    """
    db = get_db()

    try:
        result = (
            db.table("student_profiles")
            .select("*, student_progress(xp_total)")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch profile: {exc}",
        )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found. Please complete onboarding.",
        )

    row = result.data
    progress = row.get("student_progress") or {}
    if isinstance(progress, list):
        progress = progress[0] if progress else {}

    xp_total = progress.get("xp_total", 0) if isinstance(progress, dict) else 0

    # Fetch badge IDs awarded to this student
    badges: list[str] = []
    try:
        badge_result = (
            db.table("badge_awards")
            .select("badge_id")
            .eq("student_id", row["id"])
            .execute()
        )
        badges = [b["badge_id"] for b in (badge_result.data or [])]
    except Exception:
        pass

    return StudentProfileResponse(
        profile_id=row["id"],
        full_name=row["full_name"],
        class_level=row["class_level"],
        board=row["board"],
        preferred_language=row["preferred_language"],
        subjects=row.get("subjects") or [],
        xp_total=xp_total,
        badges=badges,
        created_at=row["created_at"],
    )
