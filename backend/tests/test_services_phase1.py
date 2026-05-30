import pytest

from app.services.ai_service import AIService
from app.services.session_service import SessionService


@pytest.mark.asyncio
async def test_ai_service_returns_fallback_when_no_keys(monkeypatch):
    service = AIService()
    monkeypatch.setattr(service, "_call_groq", lambda **_kwargs: (_ for _ in ()).throw(RuntimeError()))
    monkeypatch.setattr(service, "_call_gemini", lambda **_kwargs: (_ for _ in ()).throw(RuntimeError()))

    result = await service.get_response(
        student_name="Aarav",
        class_level=7,
        board="CBSE",
        language="English",
        subject="Mathematics",
        weak_topics=["Algebra"],
        context="student: hello",
        message="Can you help with linear equations?",
    )
    assert "Aarav" in result["response"]
    assert result["follow_up_question"] is not None


def test_session_service_calculate_xp():
    service = SessionService()
    assert service.calculate_xp(message_count=1) == 2
    assert service.calculate_xp(message_count=1, is_correct_answer=True) == 12
