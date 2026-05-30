"""
AI Service — wraps Groq (primary) with Gemini fallback.
"""

import asyncio
from typing import Optional
from app.core.config import settings
from groq import Groq
import google.generativeai as genai


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

    async def _call_groq(self, system_prompt: str, message: str) -> str:
        if not settings.GROQ_API_KEY:
            raise RuntimeError("Missing GROQ_API_KEY")
        client = Groq(api_key=settings.GROQ_API_KEY)
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.5,
            max_tokens=400,
        )
        content = completion.choices[0].message.content if completion.choices else ""
        if not content:
            raise RuntimeError("Empty Groq response")
        return content.strip()

    async def _call_gemini(self, system_prompt: str, message: str) -> str:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("Missing GEMINI_API_KEY")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=system_prompt,
        )
        response = await asyncio.to_thread(model.generate_content, message)
        text = getattr(response, "text", "") or ""
        if not text:
            raise RuntimeError("Empty Gemini response")
        return text.strip()

    def _extract_follow_up_question(self, text: str) -> Optional[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in reversed(lines):
            if "?" in line:
                return line
        return None

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
        """
        system_prompt = self._build_system_prompt(
            student_name=student_name,
            class_level=class_level,
            board=board,
            language=language,
            subject=subject,
            weak_topics=", ".join(weak_topics) if weak_topics else "None noted yet",
            context=context or "No prior context",
        )

        response_text = ""
        try:
            response_text = await self._call_groq(system_prompt=system_prompt, message=message)
        except Exception:
            try:
                response_text = await self._call_gemini(
                    system_prompt=system_prompt, message=message
                )
            except Exception:
                response_text = (
                    f"Great question, {student_name}! Let's solve it together step by step. "
                    "Can you share what part feels confusing?"
                )

        return {
            "response": response_text,
            "follow_up_question": self._extract_follow_up_question(response_text),
        }

    def _build_system_prompt(self, **kwargs) -> str:
        return self.SYSTEM_PROMPT_TEMPLATE.format(**kwargs)


ai_service = AIService()
