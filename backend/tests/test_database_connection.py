from app.db import database


def _reset_clients():
    database._service_client = None
    database._anon_client = None


def test_get_db_raises_with_placeholder_config(monkeypatch):
    _reset_clients()
    monkeypatch.setattr(database.settings, "SUPABASE_URL", "https://your-project-ref.supabase.co")
    monkeypatch.setattr(database.settings, "SUPABASE_SERVICE_KEY", "service-key")

    try:
        database.get_db()
        assert False, "Expected RuntimeError for placeholder SUPABASE_URL"
    except RuntimeError as exc:
        assert "SUPABASE_URL" in str(exc)


def test_get_db_initializes_and_caches_client(monkeypatch):
    _reset_clients()
    monkeypatch.setattr(database.settings, "SUPABASE_URL", "https://project.supabase.co")
    monkeypatch.setattr(database.settings, "SUPABASE_SERVICE_KEY", "service-key")

    calls = {"count": 0}

    def fake_create_client(url, key):
        calls["count"] += 1
        return {"url": url, "key": key}

    monkeypatch.setattr(database, "create_client", fake_create_client)

    first = database.get_db()
    second = database.get_db()

    assert first == second
    assert calls["count"] == 1


def test_check_db_connection_returns_error_when_db_fails(monkeypatch):
    def failing_get_db():
        raise RuntimeError("connection failed")

    monkeypatch.setattr(database, "get_db", failing_get_db)

    ok, message = database.check_db_connection()
    assert not ok
    assert "connection failed" in message
