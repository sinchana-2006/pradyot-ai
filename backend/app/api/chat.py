"""
Chat routes — sessions and messages.
"""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.chat import (
    StartSessionRequest, StartSessionResponse,
    SendMessageRequest, SendMessageResponse,
    SessionMessagesResponse, MessageRecord,
)
from app.core.dependencies import get_current_user_id
from app.db.database import get_db
from app.services.ai_service import ai_service
from app.services.session_service import session_service

router = APIRouter()


def _get_student_profile(db, user_id: str) -> dict:
    """Fetch the student profile row for a given user_id; raises 404 if missing."""
    result = (
        db.table("student_profiles")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    rows = result.data or []
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found. Please complete onboarding first.",
        )
    return rows[0]


@router.post("/session", response_model=StartSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    request: StartSessionRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Start a new chat session for a subject."""
    db = get_db()
    profile = _get_student_profile(db, user_id)

    try:
        result = db.table("chat_sessions").insert(
            {
                "student_id": profile["id"],
                "subject": request.subject,
                "topic": request.topic,
                "status": "active",
            }
        ).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {exc}",
        )

    row = result.data[0]
    return StartSessionResponse(
        session_id=row["id"],
        subject=row["subject"],
        topic=row.get("topic"),
        started_at=row["started_at"],
    )


@router.post("/message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Send a message and receive an AI tutor response.

    Steps:
    1. Verify session belongs to this student
    2. Load student profile
    3. Build conversation context
    4. Call AI service (Groq → Gemini fallback)
    5. Persist both messages
    6. Award XP and update progress
    """
    db = get_db()
    profile = _get_student_profile(db, user_id)

    # Verify session ownership
    try:
        sess_result = (
            db.table("chat_sessions")
            .select("*")
            .eq("id", request.session_id)
            .eq("student_id", profile["id"])
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify session: {exc}",
        )

    sessions = sess_result.data or []
    if not sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or does not belong to you.",
        )
    session = sessions[0]

    # Fetch progress for weak topics
    weak_topics: list[str] = []
    try:
        prog_result = (
            db.table("student_progress")
            .select("weak_topics")
            .eq("student_id", profile["id"])
            .execute()
        )
        prog_rows = prog_result.data or []
        if prog_rows:
            weak_topics = prog_rows[0].get("weak_topics") or []
    except Exception:
        pass

    # Build context from previous messages
    context = await session_service.get_context(request.session_id)

    # Call AI
    try:
        ai_result = await ai_service.get_response(
            student_name=profile["full_name"],
            class_level=profile["class_level"],
            board=profile["board"],
            language=request.language or profile.get("preferred_language", "English"),
            subject=session["subject"],
            weak_topics=weak_topics,
            context=context,
            message=request.message,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service unavailable: {exc}",
        )

    now = datetime.now(timezone.utc).isoformat()
    message_id = str(uuid.uuid4())

    # Persist student message and AI response
    try:
        db.table("messages").insert(
            [
                {
                    "session_id": request.session_id,
                    "role": "student",
                    "content": request.message,
                    "language": request.language,
                },
                {
                    "id": message_id,
                    "session_id": request.session_id,
                    "role": "assistant",
                    "content": ai_result["response"],
                    "language": request.language,
                    "xp_awarded": 2,
                },
            ]
        ).execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save messages: {exc}",
        )

    # Update session message count + XP
    xp_earned = session_service.calculate_xp(session.get("message_count", 0) + 1)
    try:
        db.table("chat_sessions").update(
            {
                "message_count": (session.get("message_count") or 0) + 2,
                "xp_earned": (session.get("xp_earned") or 0) + xp_earned,
            }
        ).eq("id", request.session_id).execute()
    except Exception:
        pass

    # Update student progress asynchronously (best-effort)
    try:
        await session_service.update_progress(
            student_id=profile["id"],
            subject=session["subject"],
            xp=xp_earned,
        )
    except Exception:
        pass

    return SendMessageResponse(
        response=ai_result["response"],
        follow_up_question=ai_result.get("follow_up_question"),
        session_id=request.session_id,
        message_id=message_id,
        xp_earned=xp_earned,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/sessions")
async def list_sessions(
    page: int = 1,
    limit: int = 10,
    subject: str | None = None,
    user_id: str = Depends(get_current_user_id),
):
    """Get the list of the student's chat sessions (newest first)."""
    db = get_db()
    profile = _get_student_profile(db, user_id)

    offset = (page - 1) * limit
    try:
        query = (
            db.table("chat_sessions")
            .select("*")
            .eq("student_id", profile["id"])
            .order("started_at", desc=True)
            .range(offset, offset + limit - 1)
        )
        if subject:
            query = query.eq("subject", subject)
        result = query.execute()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {exc}",
        )

    return {"sessions": result.data or [], "page": page, "limit": limit}


@router.get("/session/{session_id}/messages", response_model=SessionMessagesResponse)
async def get_session_messages(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Get all messages in a session (oldest first)."""
    db = get_db()
    profile = _get_student_profile(db, user_id)

    # Verify ownership
    try:
        sess_check = (
            db.table("chat_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("student_id", profile["id"])
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify session: {exc}",
        )

    if not (sess_check.data or []):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or does not belong to you.",
        )

    try:
        result = (
            db.table("messages")
            .select("*")
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .execute()
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch messages: {exc}",
        )

    messages = [
        MessageRecord(
            message_id=row["id"],
            role=row["role"],
            content=row["content"],
            timestamp=row["created_at"],
        )
        for row in (result.data or [])
    ]

    return SessionMessagesResponse(session_id=session_id, messages=messages)
