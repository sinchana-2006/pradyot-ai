"""
Chat routes — sessions and messages.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.chat import (
    StartSessionRequest, StartSessionResponse,
    SendMessageRequest, SendMessageResponse,
    SessionMessagesResponse,
)
from app.core.dependencies import get_current_user_id
from app.db.database import get_db
from app.services.ai_service import ai_service
from app.services.session_service import session_service

router = APIRouter()


def _get_student_profile(user_id: str) -> dict:
    db = get_db()
    profile_res = (
        db.table("student_profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    )
    profile = profile_res.data
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )
    return profile


@router.post("/session", response_model=StartSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    request: StartSessionRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Start a new chat session for a subject.
    """
    try:
        db = get_db()
        profile = _get_student_profile(user_id)
        insert_res = (
            db.table("chat_sessions")
            .insert(
                {
                    "student_id": profile["id"],
                    "subject": request.subject,
                    "topic": request.topic,
                }
            )
            .execute()
        )
        session = (insert_res.data or [None])[0]
        if not session:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create chat session",
            )
        return StartSessionResponse(
            session_id=session["id"],
            subject=session["subject"],
            topic=session.get("topic"),
            started_at=session["started_at"],
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to start chat session",
        ) from exc


@router.post("/message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Send a message and receive an AI tutor response.
    """
    try:
        db = get_db()
        profile = _get_student_profile(user_id)
        session_res = (
            db.table("chat_sessions")
            .select("*")
            .eq("id", request.session_id)
            .eq("student_id", profile["id"])
            .maybe_single()
            .execute()
        )
        session = session_res.data
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found",
            )

        student_message_res = (
            db.table("messages")
            .insert(
                {
                    "session_id": request.session_id,
                    "role": "student",
                    "content": request.message,
                    "language": request.language,
                }
            )
            .execute()
        )
        student_message = (student_message_res.data or [None])[0]

        progress_res = (
            db.table("student_progress")
            .select("weak_topics,total_messages")
            .eq("student_id", profile["id"])
            .maybe_single()
            .execute()
        )
        progress = progress_res.data or {}

        context = await session_service.get_context(request.session_id)
        ai_result = await ai_service.get_response(
            student_name=profile["full_name"],
            class_level=profile["class_level"],
            board=profile["board"],
            language=request.language or profile.get("preferred_language", "English"),
            subject=session["subject"],
            weak_topics=progress.get("weak_topics") or [],
            context=context,
            message=request.message,
        )

        xp_earned = session_service.calculate_xp(
            message_count=int(progress.get("total_messages", 0)) + 1
        )
        assistant_message_res = (
            db.table("messages")
            .insert(
                {
                    "session_id": request.session_id,
                    "role": "assistant",
                    "content": ai_result["response"],
                    "language": request.language,
                    "xp_awarded": xp_earned,
                }
            )
            .execute()
        )
        assistant_message = (assistant_message_res.data or [None])[0]
        if not assistant_message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to store AI response",
            )

        db.table("chat_sessions").update(
            {
                "message_count": int(session.get("message_count", 0)) + 2,
                "xp_earned": int(session.get("xp_earned", 0)) + xp_earned,
            }
        ).eq("id", session["id"]).execute()
        await session_service.update_progress(
            student_id=profile["id"], subject=session["subject"], xp=xp_earned
        )

        return SendMessageResponse(
            response=ai_result["response"],
            follow_up_question=ai_result.get("follow_up_question"),
            session_id=request.session_id,
            message_id=assistant_message["id"],
            xp_earned=xp_earned,
            timestamp=assistant_message["created_at"],
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to process message",
        ) from exc


@router.get("/sessions")
async def list_sessions(
    page: int = 1,
    limit: int = 10,
    subject: str | None = None,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get the list of the student's chat sessions.
    """
    if page < 1 or limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pagination")
    try:
        db = get_db()
        profile = _get_student_profile(user_id)
        query = (
            db.table("chat_sessions")
            .select("*")
            .eq("student_id", profile["id"])
            .order("started_at", desc=True)
        )
        if subject:
            query = query.eq("subject", subject)
        offset = (page - 1) * limit
        res = query.range(offset, offset + limit - 1).execute()
        sessions = [
            {
                "session_id": row["id"],
                "subject": row["subject"],
                "topic": row.get("topic"),
                "message_count": row.get("message_count", 0),
                "xp_earned": row.get("xp_earned", 0),
                "started_at": row.get("started_at"),
                "ended_at": row.get("ended_at"),
            }
            for row in (res.data or [])
        ]
        return {"sessions": sessions, "total": len(sessions), "page": page, "limit": limit}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch sessions",
        ) from exc


@router.get("/session/{session_id}/messages", response_model=SessionMessagesResponse)
async def get_session_messages(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get all messages in a session.
    """
    try:
        db = get_db()
        profile = _get_student_profile(user_id)
        session_res = (
            db.table("chat_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("student_id", profile["id"])
            .maybe_single()
            .execute()
        )
        if not session_res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found",
            )
        messages_res = (
            db.table("messages")
            .select("*")
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .execute()
        )
        messages = [
            {
                "message_id": msg["id"],
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["created_at"],
            }
            for msg in (messages_res.data or [])
        ]
        return SessionMessagesResponse(session_id=session_id, messages=messages)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch session messages",
        ) from exc
