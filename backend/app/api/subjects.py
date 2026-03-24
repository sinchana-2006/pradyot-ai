"""
Subjects route — list available subjects by class and board.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user_id

router = APIRouter()

# Static subject data for Phase 0 — will be driven by DB in Phase 1
SUBJECTS_BY_CLASS = {
    range(1, 4): ["English", "Mathematics", "Environmental Studies", "Hindi"],
    range(4, 6): ["English", "Mathematics", "Science", "Social Studies", "Hindi"],
    range(6, 9): ["English", "Mathematics", "Science", "Social Studies", "Hindi", "Sanskrit"],
    range(9, 11): [
        "English",
        "Mathematics",
        "Science",
        "Social Science",
        "Hindi",
        "Sanskrit",
        "Information Technology",
    ],
}


def get_subjects_for_class(class_level: int) -> list[str]:
    for class_range, subjects in SUBJECTS_BY_CLASS.items():
        if class_level in class_range:
            return subjects
    return []


@router.get("")
async def list_subjects(
    class_level: int,
    board: str | None = None,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get available subjects for a class level.

    Returns static subject list for Phase 0.
    TODO (Phase 1): Drive from database with board-specific curricula.
    """
    if class_level < 1 or class_level > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="class_level must be between 1 and 10",
        )
    subjects = get_subjects_for_class(class_level)
    return {
        "class_level": class_level,
        "board": board or "CBSE",
        "subjects": [{"subject_id": s.lower().replace(" ", "_"), "name": s} for s in subjects],
    }
