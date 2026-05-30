"""
Session Service — manages conversation context and XP calculation.
"""

from datetime import date
from app.db.database import get_db

class SessionService:
    """
    Manages chat session state, context windows, and gamification.

    TODO (Phase 1): Implement with Supabase integration.
    """

    MAX_CONTEXT_MESSAGES = 10  # Number of messages to include in AI context

    async def get_context(self, session_id: str) -> str:
        """
        Retrieve the last N messages from a session for AI context.
        """
        db = get_db()
        res = (
            db.table("messages")
            .select("role,content,created_at")
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .limit(self.MAX_CONTEXT_MESSAGES)
            .execute()
        )
        lines = []
        for row in (res.data or []):
            role = row.get("role", "unknown")
            content = row.get("content", "")
            lines.append(f"{role}: {content}")
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
        Update student progress after a session interaction.
        """
        db = get_db()
        current = (
            db.table("student_progress")
            .select("*")
            .eq("student_id", student_id)
            .maybe_single()
            .execute()
        ).data
        today = date.today()

        if not current:
            subject_stats = {subject: {"sessions": 1, "xp": xp, "strength": "low"}}
            db.table("student_progress").insert(
                {
                    "student_id": student_id,
                    "xp_total": xp,
                    "xp_this_week": xp,
                    "study_streak_days": 1,
                    "last_active_date": str(today),
                    "subject_stats": subject_stats,
                    "total_sessions": 1,
                    "total_messages": 1,
                }
            ).execute()
            return

        last_active = current.get("last_active_date")
        streak = current.get("study_streak_days", 0)
        if last_active:
            delta = (today - date.fromisoformat(last_active)).days
            if delta == 1:
                streak += 1
            elif delta > 1:
                streak = 1
        else:
            streak = 1

        subject_stats = current.get("subject_stats") or {}
        entry = subject_stats.get(subject, {"sessions": 0, "xp": 0, "strength": "low"})
        entry["sessions"] = int(entry.get("sessions", 0)) + 1
        entry["xp"] = int(entry.get("xp", 0)) + xp
        if entry["xp"] >= 120:
            entry["strength"] = "high"
        elif entry["xp"] >= 50:
            entry["strength"] = "medium"
        else:
            entry["strength"] = "low"
        subject_stats[subject] = entry

        db.table("student_progress").update(
            {
                "xp_total": int(current.get("xp_total", 0)) + xp,
                "xp_this_week": int(current.get("xp_this_week", 0)) + xp,
                "study_streak_days": streak,
                "last_active_date": str(today),
                "subject_stats": subject_stats,
                "total_messages": int(current.get("total_messages", 0)) + 1,
            }
        ).eq("student_id", student_id).execute()


session_service = SessionService()
