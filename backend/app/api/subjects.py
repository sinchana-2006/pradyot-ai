"""
Subjects route — list available subjects by class and board.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user_id
from app.db.database import get_db

router = APIRouter()

def _slugify_subject(subject: str) -> str:
    return subject.lower().strip().replace(" ", "_")


@router.get("")
async def list_subjects(
    class_level: int,
    board: str | None = None,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get available subjects for a class level.
    """
    if class_level < 1 or class_level > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="class_level must be between 1 and 10",
        )

    db = get_db()
    selected_board = board
    if not selected_board:
        try:
            profile_result = (
                db.table("student_profiles")
                .select("board")
                .eq("user_id", user_id)
                .limit(1)
                .execute()
            )
            profile_rows = profile_result.data or []
            if profile_rows:
                selected_board = profile_rows[0].get("board")
        except Exception:
            selected_board = None

    selected_board = selected_board or "CBSE"

    try:
        pyq_result = (
            db.table("pyq_questions")
            .select("subject")
            .eq("class_level", class_level)
            .eq("board", selected_board)
            .execute()
        )
        subject_rows = pyq_result.data or []
        subjects = sorted(
            {
                row["subject"].strip()
                for row in subject_rows
                if row.get("subject") and row["subject"].strip()
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load subjects: {exc}",
        )

    # Fallback to student's own selected subjects if no PYQ subject metadata exists yet.
    if not subjects:
        try:
            profile_subjects_result = (
                db.table("student_profiles")
                .select("subjects")
                .eq("user_id", user_id)
                .limit(1)
                .execute()
            )
            rows = profile_subjects_result.data or []
            subjects = sorted(rows[0].get("subjects") or []) if rows else []
        except Exception:
            subjects = []

    return {
        "class_level": class_level,
        "board": selected_board,
        "subjects": [{"subject_id": _slugify_subject(s), "name": s} for s in subjects],
    }
