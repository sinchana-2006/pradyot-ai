from app.api.pyq import _normalize_text, _is_answer_correct


def test_normalize_text():
    assert _normalize_text("  Water   boils At 100C  ") == "water boils at 100c"


def test_answer_correct_when_student_contains_key_phrase():
    assert _is_answer_correct("The answer is photosynthesis", "photosynthesis")


def test_answer_incorrect_when_text_differs():
    assert not _is_answer_correct("evaporation", "condensation")

