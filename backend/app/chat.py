"""
Groq API integration for PradyotAI chat.
Handles AI responses with Indian context and adaptive teaching style.
"""

import os
from pathlib import Path
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

from app.models import StudentOnboarding, ChatMessage

# Load .env from project root using python-dotenv
# Path: pradyot-ai/.env (works regardless of CWD when running uvicorn)
_project_root = Path(__file__).resolve().parent.parent.parent
_env_file = _project_root / ".env"
load_dotenv(dotenv_path=_env_file, override=False)  # override=False: don't overwrite existing env vars

# System prompt for PradyotAI - defines the tutor's personality and behavior
PRADYOT_SYSTEM_PROMPT = """You are PradyotAI, a friendly and patient personal tutor for Indian school students. 
Adapt your language and explanation style based on the student's class level. 
Use simple Indian examples like cricket, chai, festivals. 
Never make the student feel stupid. 
End every response with one follow up question. 
If student says they dont understand, explain differently. 
Respond in whatever language the student writes in."""


def _get_api_key() -> str:
    """Get Groq API key from environment. Never hardcode."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found in environment. Add it to .env")
    return key


def _build_context_prompt(student_context: Optional[StudentOnboarding]) -> str:
    """
    Build context string from student profile for personalized responses.
    """
    if not student_context:
        return ""
    return f"""
Student Profile:
- Name: {student_context.name}
- Class: {student_context.class_level}
- Board: {student_context.board}
- Subject: {student_context.subject}
- Preferred Language: {student_context.preferred_language}

Use this context to tailor your explanations. Keep explanations appropriate for Class {student_context.class_level}.
"""


def get_chat_response(
    message: str,
    student_context: Optional[StudentOnboarding] = None,
    history: list[ChatMessage] = None
) -> str:
    """
    Send message to Groq and return PradyotAI's response.

    Args:
        message: The student's message
        student_context: Optional student profile for personalization
        history: Optional list of previous messages for conversation context

    Returns:
        AI response string
    """
    client = Groq(api_key=_get_api_key())

    # Build messages: system + history + current user message
    system_content = PRADYOT_SYSTEM_PROMPT + _build_context_prompt(student_context)
    messages = [{"role": "system", "content": system_content}]

    # Add conversation history (last 10 messages)
    history = history or []
    for msg in history[-10:]:
        role = "user" if msg.role == "user" else "assistant"
        messages.append({"role": role, "content": msg.content})

    # Add current user message
    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )

    return completion.choices[0].message.content
