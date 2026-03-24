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

router = APIRouter()


@router.post("/session", response_model=StartSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    request: StartSessionRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Start a new chat session for a subject.

    TODO (Phase 1): Create session record in Supabase.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Chat sessions not yet implemented — Phase 1",
    )


@router.post("/message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    user_id: str = Depends(get_current_user_id),
):
    """
    Send a message and receive an AI tutor response.

    TODO (Phase 1):
    1. Load student profile + session context from Supabase
    2. Build system prompt with student details
    3. Call Groq API (fall back to Gemini)
    4. Save messages to Supabase
    5. Update XP and progress
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="AI chat not yet implemented — Phase 1",
    )


@router.get("/sessions")
async def list_sessions(
    page: int = 1,
    limit: int = 10,
    subject: str | None = None,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get the list of the student's chat sessions.

    TODO (Phase 1): Query Supabase chat_sessions table.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session listing not yet implemented — Phase 1",
    )


@router.get("/session/{session_id}/messages", response_model=SessionMessagesResponse)
async def get_session_messages(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """
    Get all messages in a session.

    TODO (Phase 1): Query Supabase messages table.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session messages not yet implemented — Phase 1",
    )
