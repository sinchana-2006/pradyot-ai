"""
Pydantic models for request/response validation.
All data structures used by the API are defined here.
"""

from pydantic import BaseModel, Field
from typing import Optional


# --- Student Onboarding Models ---

class StudentOnboarding(BaseModel):
    """Data collected during student onboarding."""
    name: str = Field(..., min_length=1, max_length=100, description="Student's name")
    class_level: int = Field(..., ge=1, le=10, description="Class 1-10")
    board: str = Field(..., min_length=1, max_length=50, description="CBSE, ICSE, or State Board name")
    subject: str = Field(..., min_length=1, max_length=100, description="Subject of focus")
    preferred_language: str = Field(..., min_length=1, max_length=50, description="e.g., English, Hindi")


# --- Chat Models ---

class ChatMessage(BaseModel):
    """Single message in a chat conversation."""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Incoming chat request from frontend."""
    message: str = Field(..., min_length=1, max_length=4000, description="Student's message")
    student_id: Optional[str] = Field(default=None, description="UUID of student for saving chat history")
    student_context: Optional[StudentOnboarding] = Field(
        default=None,
        description="Student profile for personalized responses"
    )
    history: list[ChatMessage] = Field(
        default_factory=list,
        description="Previous messages for context"
    )


class ChatResponse(BaseModel):
    """Response from the AI chat."""
    message: str = Field(..., description="PradyotAI's response")
    success: bool = Field(default=True, description="Whether the request succeeded")
