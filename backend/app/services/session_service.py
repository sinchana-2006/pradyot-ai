"""
Session Service — manages conversation context and XP calculation.
"""

import logging
from datetime import date
from app.db.database import get_db

logger = logging.getLogger(__name__)


class SessionService:
    """
    Manages chat session state, context windows, and gamification.
    """

    MAX_CONTEXT_MESSAGES = 10  # Number of recent messages to include in AI context

    async def get_context(self, session_id: str) -> str:
        """
        Retrieve the last N messages from a session and format them as context text.
        """
        db = get_db()
        try:
            result = (
                db.table("messages")
                .select("role, content")
                .eq("session_id", session_id)
                .order("created_at", desc=False)
                .limit(self.MAX_CONTEXT_MESSAGES)
                .execute()
            )
            rows = result.data or []
        except Exception as exc:
            logger.warning("Could not load session context: %s", exc)
            return ""

        if not rows:
            return ""

        lines = []
        for row in rows:
            role_label = "Student" if row["role"] == "student" else "Pradyot"
            lines.append(f"{role_label}: {row['content']}")
        return "\n".join(lines)

    def calculate_xp(self, message_count: int, is_correct_answer: bool = False) -> int:
        """
        Calculate XP earned for a chat interaction.

        Base XP per message: 2
        Correct answer bonus: 10
        """
        xp = 2
        if is_correct_answer:
            xp += 10
        return xp

    async def update_progress(self, student_id: str, subject: str, xp: int) -> None:
        """
        Upsert student_progress: increment XP totals, update last_active_date,
        and update per-subject stats.
        """
        db = get_db()
        try:
            # Fetch existing progress row
            result = (
                db.table("student_progress")
                .select("*")
                .eq("student_id", student_id)
                .execute()
            )
            rows = result.data or []

            if rows:
                row = rows[0]
                subject_stats: dict = row.get("subject_stats") or {}
                stats = subject_stats.get(subject, {"sessions": 0, "xp": 0})
                stats["xp"] = stats.get("xp", 0) + xp
                subject_stats[subject] = stats

                db.table("student_progress").update(
                    {
                        "xp_total": (row.get("xp_total") or 0) + xp,
                        "xp_this_week": (row.get("xp_this_week") or 0) + xp,
                        "total_messages": (row.get("total_messages") or 0) + 1,
                        "last_active_date": date.today().isoformat(),
                        "subject_stats": subject_stats,
                    }
                ).eq("student_id", student_id).execute()
            else:
                # Create progress row with all default fields
                db.table("student_progress").insert(
                    {
                        "student_id": student_id,
                        "xp_total": xp,
                        "xp_this_week": xp,
                        "xp_this_month": xp,
                        "study_streak_days": 0,
                        "total_sessions": 0,
                        "total_messages": 1,
                        "last_active_date": date.today().isoformat(),
                        "subject_stats": {subject: {"sessions": 0, "xp": xp}},
                        "weak_topics": [],
                        "strong_topics": [],
                    }
                ).execute()
        except Exception as exc:
            logger.warning("Could not update student progress: %s", exc)


session_service = SessionService()
