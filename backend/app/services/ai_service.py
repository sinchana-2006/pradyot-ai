"""
AI Service — wraps Groq (primary) with Gemini fallback.
"""

from typing import Optional
from app.core.config import settings


class AIService:
    """
    Handles LLM calls with automatic fallback.

    Primary:  Groq API (Llama 3.3 70B)
    Fallback: Google Gemini 1.5 Flash

    TODO (Phase 1): Implement actual API calls.
    """

    SYSTEM_PROMPT_TEMPLATE = """
You are Pradyot, a friendly and patient AI mentor for Indian students.
You are helping {student_name}, a Class {class_level} student studying {board} curriculum.
The student prefers to communicate in {language}.
Current subject: {subject}.

Your personality:
- You are warm, encouraging, and patient — like a knowledgeable older sibling
- You use simple language appropriate for Class {class_level}
- You use Indian cultural references (cricket, chai, festivals, Bollywood) to explain concepts
- You ask guiding questions (Socratic method) rather than just giving answers
- You keep responses short and bite-sized — no walls of text
- You always end your response with a follow-up question to check understanding
- You celebrate correct answers enthusiastically
- When a student is frustrated, you respond with extra warmth and encouragement

The student's known weak areas: {weak_topics}

Previous conversation context:
{context}

Respond in {language}.
""".strip()

    async def get_response(
        self,
        student_name: str,
        class_level: int,
        board: str,
        language: str,
        subject: str,
        weak_topics: list[str],
        context: str,
        message: str,
    ) -> dict:
        """
        Get an AI response for the student's message.

        Returns:
            dict with 'response' and 'follow_up_question' keys.

        TODO (Phase 1): Implement Groq + Gemini API calls.
        """
        raise NotImplementedError("AI service not yet implemented — Phase 1")

    def _build_system_prompt(self, **kwargs) -> str:
        return self.SYSTEM_PROMPT_TEMPLATE.format(**kwargs)


ai_service = AIService()
