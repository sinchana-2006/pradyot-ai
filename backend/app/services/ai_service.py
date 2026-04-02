"""
AI Service — wraps Groq (primary) with Gemini fallback.
"""

import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """
    Handles LLM calls with automatic fallback.

    Primary:  Groq API (Llama 3.3 70B)
    Fallback: Google Gemini 1.5 Flash
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

        Tries Groq first; falls back to Gemini on any error.

        Returns:
            dict with 'response' and 'follow_up_question' keys.
        """
        system_prompt = self._build_system_prompt(
            student_name=student_name,
            class_level=class_level,
            board=board,
            language=language,
            subject=subject,
            weak_topics=", ".join(weak_topics) if weak_topics else "None identified yet",
            context=context or "This is the start of the conversation.",
        )

        # Try Groq first
        if settings.GROQ_API_KEY:
            try:
                return await self._call_groq(system_prompt, message)
            except Exception as exc:
                logger.warning("Groq API failed, falling back to Gemini: %s", exc)

        # Fall back to Gemini
        if settings.GEMINI_API_KEY:
            try:
                return await self._call_gemini(system_prompt, message)
            except Exception as exc:
                logger.error("Gemini API also failed: %s", exc)
                raise

        raise RuntimeError(
            "No AI API keys configured. Please set GROQ_API_KEY or GEMINI_API_KEY."
        )

    async def _call_groq(self, system_prompt: str, message: str) -> dict:
        """Call the Groq API (Llama 3.3 70B)."""
        from groq import Groq  # lazy import to avoid startup errors when key is absent

        client = Groq(api_key=settings.GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.7,
            max_tokens=512,
        )
        text = completion.choices[0].message.content or ""
        return self._parse_response(text)

    async def _call_gemini(self, system_prompt: str, message: str) -> dict:
        """Call the Google Gemini API as a fallback."""
        import google.generativeai as genai  # lazy import

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=system_prompt,
        )
        response = model.generate_content(message)
        text = response.text or ""
        return self._parse_response(text)

    def _parse_response(self, text: str) -> dict:
        """
        Split the AI response into main content and follow-up question.
        The last sentence ending with '?' is treated as the follow-up.
        """
        text = text.strip()
        sentences = [s.strip() for s in text.replace("?", "?\n").split("\n") if s.strip()]

        follow_up: Optional[str] = None
        if sentences and sentences[-1].endswith("?"):
            follow_up = sentences[-1]
            response_body = text[: text.rfind(follow_up)].strip()
            if not response_body:
                response_body = text
        else:
            response_body = text

        return {"response": response_body, "follow_up_question": follow_up}

    def _build_system_prompt(self, **kwargs) -> str:
        return self.SYSTEM_PROMPT_TEMPLATE.format(**kwargs)


ai_service = AIService()
