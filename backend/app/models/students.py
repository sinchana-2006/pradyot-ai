"""
Pydantic schemas for Student endpoints.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StudentProfileRequest(BaseModel):
    full_name: str
    class_level: int
    board: str
    preferred_language: str = "English"
    subjects: List[str] = []
    state: Optional[str] = None


class StudentProfileResponse(BaseModel):
    profile_id: str
    full_name: str
    class_level: int
    board: str
    preferred_language: str
    subjects: List[str]
    xp_total: int = 0
    badges: List[str] = []
    created_at: datetime
