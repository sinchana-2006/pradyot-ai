"""
Session Service — manages conversation context and XP calculation.
"""


class SessionService:
    """
    Manages chat session state, context windows, and gamification.

    TODO (Phase 1): Implement with Supabase integration.
    """

    MAX_CONTEXT_MESSAGES = 10  # Number of messages to include in AI context

    async def get_context(self, session_id: str) -> str:
        """
        Retrieve the last N messages from a session for AI context.

        TODO (Phase 1): Query Supabase messages table.
        """
        raise NotImplementedError("Session service not yet implemented — Phase 1")

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

        TODO (Phase 1): Update Supabase student_progress table.
        """
        raise NotImplementedError("Session service not yet implemented — Phase 1")


session_service = SessionService()
