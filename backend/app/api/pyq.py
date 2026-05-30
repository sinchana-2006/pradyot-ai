"""
PYQ (Previous Year Questions) routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.pyq import PYQListResponse, CheckAnswerRequest, CheckAnswerResponse
from app.core.dependencies import get_current_user_id
from app.db.database import get_db
from app.services.session_service import session_service

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
    """
    if page < 1 or limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pagination")
    try:
        db = get_db()
        query = (
            db.table("pyq_questions")
            .select("*")
            .eq("subject", subject)
            .eq("class_level", class_level)
            .order("year", desc=True)
        )
        if year:
            query = query.eq("year", year)
        if chapter:
            query = query.ilike("chapter", f"%{chapter}%")
        if difficulty:
            query = query.eq("difficulty", difficulty)
        offset = (page - 1) * limit
        res = query.range(offset, offset + limit - 1).execute()
        questions = [
            {
                "question_id": row["id"],
                "subject": row["subject"],
                "class_level": row["class_level"],
                "year": row.get("year"),
                "chapter": row.get("chapter"),
                "question_text": row["question_text"],
                "marks": row.get("marks"),
                "difficulty": row.get("difficulty"),
                "board": row["board"],
            }
            for row in (res.data or [])
        ]
        return PYQListResponse(questions=questions, total=len(questions), page=page, limit=limit)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch PYQ questions",
        ) from exc


@router.post("/check-answer", response_model=CheckAnswerResponse)
async def check_answer(
    request: CheckAnswerRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Check a student's answer to a PYQ and provide feedback.
    """
    try:
        db = get_db()
        profile_res = (
            db.table("student_profiles")
            .select("id")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
        profile = profile_res.data
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        question_res = (
            db.table("pyq_questions")
            .select("*")
            .eq("id", request.question_id)
            .maybe_single()
            .execute()
        )
        question = question_res.data
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

        answer_key = (question.get("answer_key") or "").strip()
        given_answer = (request.student_answer or "").strip()
        is_correct = bool(answer_key) and answer_key.lower() == given_answer.lower()
        xp_earned = 10 if is_correct else 2

        if is_correct:
            feedback = "Excellent work! Your answer is correct."
            explanation = "Great job applying the correct concept."
        else:
            feedback = "Good attempt. Review the correct method and try once more."
            explanation = "Compare your approach with the expected key steps and final answer."

        db.table("pyq_attempts").insert(
            {
                "student_id": profile["id"],
                "question_id": request.question_id,
                "session_id": request.session_id,
                "student_answer": request.student_answer,
                "is_correct": is_correct,
                "ai_feedback": feedback,
                "xp_awarded": xp_earned,
            }
        ).execute()
        await session_service.update_progress(
            student_id=profile["id"], subject=question["subject"], xp=xp_earned
        )

        return CheckAnswerResponse(
            is_correct=is_correct,
            feedback=feedback,
            correct_answer=answer_key or "Answer key unavailable",
            explanation=explanation,
            xp_earned=xp_earned,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to evaluate PYQ answer",
        ) from exc
