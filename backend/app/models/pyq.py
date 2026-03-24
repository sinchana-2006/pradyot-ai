"""
Pydantic schemas for PYQ endpoints.
"""

from pydantic import BaseModel
from typing import Optional, List


class PYQQuestion(BaseModel):
    question_id: str
    subject: str
    class_level: int
    year: Optional[int]
    chapter: Optional[str]
    question_text: str
    marks: Optional[int]
    difficulty: Optional[str]
    board: str


class PYQListResponse(BaseModel):
    questions: List[PYQQuestion]
    total: int
    page: int
    limit: int


class CheckAnswerRequest(BaseModel):
    question_id: str
    student_answer: str
    session_id: Optional[str] = None


class CheckAnswerResponse(BaseModel):
    is_correct: bool
    feedback: str
    correct_answer: str
    explanation: str
    xp_earned: int
