from app.api.subjects import _slugify_subject


def test_slugify_subject():
    assert _slugify_subject("Social Science") == "social_science"
    assert _slugify_subject("  Mathematics  ") == "mathematics"

