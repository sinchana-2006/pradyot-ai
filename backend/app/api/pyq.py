"""
PYQ (Previous Year Questions) routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.pyq import PYQListResponse, CheckAnswerRequest, CheckAnswerResponse
from app.core.dependencies import get_current_user_id
from app.db.database import get_db
from app.services.ai_service import ai_service
from app.services.session_service import session_service

router = APIRouter()

def _normalize_text(text: str | None) -> str:
    return " ".join((text or "").lower().strip().split())


def _is_answer_correct(student_answer: str, answer_key: str) -> bool:
    student = _normalize_text(student_answer)
    key = _normalize_text(answer_key)
    if not student or not key:
        return False
    return student in key or key in student


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page and limit must be greater than 0",
        )

    db = get_db()
    offset = (page - 1) * limit

    # Infer student's board for consistent filtering.
    student_board = None
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
            student_board = profile_rows[0].get("board")
    except Exception:
        student_board = None

    try:
        query = (
            db.table("pyq_questions")
            .select("*", count="exact")
            .eq("subject", subject)
            .eq("class_level", class_level)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
        )
        if year is not None:
            query = query.eq("year", year)
        if chapter:
            query = query.ilike("chapter", f"%{chapter}%")
        if difficulty:
            query = query.eq("difficulty", difficulty)
        if student_board:
            query = query.eq("board", student_board)
        result = query.execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch PYQ questions: {exc}",
        )

    rows = result.data or []
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
        for row in rows
    ]
    return {
        "questions": questions,
        "total": int(result.count or 0),
        "page": page,
        "limit": limit,
    }


@router.post("/check-answer", response_model=CheckAnswerResponse)
async def check_answer(
    request: CheckAnswerRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Check a student's answer to a PYQ and provide AI feedback.
    """
    db = get_db()

    # Resolve student profile for ownership and personalization.
    try:
        profile_result = (
            db.table("student_profiles")
            .select("*")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        profile_rows = profile_result.data or []
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch student profile: {exc}",
        )

    if not profile_rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found. Please complete onboarding first.",
        )
    student = profile_rows[0]

    # Fetch question and answer key.
    try:
        question_result = (
            db.table("pyq_questions")
            .select("*")
            .eq("id", request.question_id)
            .single()
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question not found: {exc}",
        )

    question = question_result.data
    answer_key = (question.get("answer_key") or "").strip()
    if not answer_key:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Answer key missing for this question.",
        )

    is_correct = _is_answer_correct(request.student_answer, answer_key)
    xp_earned = session_service.calculate_xp(message_count=1, is_correct_answer=is_correct)

    feedback_prompt = (
        "Evaluate this student's answer.\n"
        f"Question: {question['question_text']}\n"
        f"Official answer: {answer_key}\n"
        f"Student answer: {request.student_answer}\n"
        "Give concise feedback in 3-5 lines, mention one strength and one improvement."
    )
    try:
        ai_eval = await ai_service.get_response(
            student_name=student["full_name"],
            class_level=student["class_level"],
            board=student["board"],
            language=student.get("preferred_language", "English"),
            subject=question["subject"],
            weak_topics=[],
            context="PYQ answer evaluation",
            message=feedback_prompt,
        )
        feedback = ai_eval.get("response") or "Good attempt. Keep practicing!"
    except Exception:
        if is_correct:
            feedback = "Great work! Your answer is correct."
        else:
            feedback = "Good attempt. Revise the key concepts and try again."

    explanation = (
        "Matched closely with answer key."
        if is_correct
        else "Your answer differs from the official key. Compare key points and improve."
    )

    # Record attempt
    try:
        db.table("pyq_attempts").insert(
            {
                "student_id": student["id"],
                "question_id": request.question_id,
                "session_id": request.session_id,
                "student_answer": request.student_answer,
                "is_correct": is_correct,
                "ai_feedback": feedback,
                "xp_awarded": xp_earned,
            }
        ).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save attempt: {exc}",
        )

    try:
        await session_service.update_progress(
            student_id=student["id"],
            subject=question["subject"],
            xp=xp_earned,
        )
    except Exception:
        pass

    return CheckAnswerResponse(
        is_correct=is_correct,
        feedback=feedback,
        correct_answer=answer_key,
        explanation=explanation,
        xp_earned=xp_earned,
    )
