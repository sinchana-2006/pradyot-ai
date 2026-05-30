"""
Student profile routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.models.students import StudentProfileRequest, StudentProfileResponse
from app.core.dependencies import get_current_user_id
from app.db.database import get_db

router = APIRouter()


def _build_profile_response(
    profile: dict, xp_total: int = 0, badges: Optional[List[str]] = None
):
    return StudentProfileResponse(
        profile_id=profile["id"],
        full_name=profile["full_name"],
        class_level=profile["class_level"],
        board=profile["board"],
        preferred_language=profile.get("preferred_language", "English"),
        subjects=profile.get("subjects", []),
        xp_total=xp_total,
        badges=badges or [],
        created_at=profile["created_at"],
    )


@router.post("/profile", response_model=StudentProfileResponse)
async def create_or_update_profile(
    request: StudentProfileRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Create or update the student's academic profile in Supabase.
    """
    try:
        db = get_db()
        payload = {
            "user_id": user_id,
            "full_name": request.full_name,
            "class_level": request.class_level,
            "board": request.board,
            "state": request.state,
            "preferred_language": request.preferred_language,
            "subjects": request.subjects,
        }
        upsert_res = (
            db.table("student_profiles")
            .upsert(payload, on_conflict="user_id")
            .execute()
        )
        data = upsert_res.data or []
        if not data:
            profile_res = (
                db.table("student_profiles")
                .select("*")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            profile = profile_res.data
        else:
            profile = data[0]

        db.table("student_progress").upsert(
            {"student_id": profile["id"]}, on_conflict="student_id"
        ).execute()
        return _build_profile_response(profile)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to save student profile",
        ) from exc


@router.get("/profile", response_model=StudentProfileResponse)
async def get_profile(user_id: str = Depends(get_current_user_id)):
    """
    Get the current student's profile from Supabase.
    """
    try:
        db = get_db()
        profile_res = (
            db.table("student_profiles")
            .select("*")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        profile = profile_res.data
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        progress_res = (
            db.table("student_progress")
            .select("xp_total")
            .eq("student_id", profile["id"])
            .maybe_single()
            .execute()
        )
        badges_res = (
            db.table("badge_awards")
            .select("badge_id")
            .eq("student_id", profile["id"])
            .execute()
        )
        xp_total = (progress_res.data or {}).get("xp_total", 0)
        badges = [row["badge_id"] for row in (badges_res.data or [])]
        return _build_profile_response(profile, xp_total=xp_total, badges=badges)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch student profile",
        ) from exc
