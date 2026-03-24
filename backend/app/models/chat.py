"""
Pydantic schemas for Chat endpoints.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StartSessionRequest(BaseModel):
    subject: str
    topic: Optional[str] = None


class StartSessionResponse(BaseModel):
    session_id: str
    subject: str
    topic: Optional[str]
    started_at: datetime


class SendMessageRequest(BaseModel):
    session_id: str
    message: str
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
