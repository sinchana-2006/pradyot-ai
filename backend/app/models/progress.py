"""
Pydantic schemas for Progress endpoints.
"""

from pydantic import BaseModel
from typing import Dict, List, Any


class SubjectStat(BaseModel):
    sessions: int
    xp: int
    strength: str  # "low" | "medium" | "high"


class ProgressSummaryResponse(BaseModel):
    student_name: str
    xp_total: int
    xp_this_week: int
    study_streak_days: int
    badges: List[str]
    subjects_covered: Dict[str, Any]
    weak_topics: List[str]
    strong_topics: List[str]
