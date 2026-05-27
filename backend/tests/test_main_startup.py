import pytest

import main


def test_ensure_db_ready_on_startup_success(monkeypatch):
    monkeypatch.setattr(main, "check_db_connection", lambda: (True, "ok"))
    main.ensure_db_ready_on_startup()


def test_ensure_db_ready_on_startup_failure(monkeypatch):
    monkeypatch.setattr(main, "check_db_connection", lambda: (False, "connection unavailable"))
    with pytest.raises(RuntimeError, match="Database connection failed during startup."):
        main.ensure_db_ready_on_startup()
