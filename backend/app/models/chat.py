"""
Pydantic schemas for Chat endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StartSessionRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=50)
    topic: Optional[str] = None


class StartSessionResponse(BaseModel):
    session_id: str
    subject: str
    topic: Optional[str]
    started_at: datetime


class SendMessageRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1)
    language: Optional[str] = "English"


class SendMessageResponse(BaseModel):
    response: str
    follow_up_question: Optional[str]
    session_id: str
    message_id: str
    xp_earned: int = 0
    timestamp: datetime


class MessageRecord(BaseModel):
    message_id: str
    role: str
    content: str
    timestamp: datetime


class SessionMessagesResponse(BaseModel):
    session_id: str
    messages: list[MessageRecord]


class SessionSummary(BaseModel):
    session_id: str
    subject: str
    topic: Optional[str]
    message_count: int
    xp_earned: int
    started_at: datetime
    ended_at: Optional[datetime]


class SessionListResponse(BaseModel):
    sessions: list[SessionSummary]
    total: int
    page: int
    limit: int
