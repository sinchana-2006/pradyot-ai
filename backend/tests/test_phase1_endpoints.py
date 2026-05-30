from types import SimpleNamespace
from fastapi.testclient import TestClient
from main import app


class FakeQuery:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.operation = None
        self.payload = None
        self.filters = {}

    def select(self, *_args, **_kwargs):
        self.operation = "select"
        return self

    def insert(self, payload):
        self.operation = "insert"
        self.payload = payload
        return self

    def upsert(self, payload, **_kwargs):
        self.operation = "upsert"
        self.payload = payload
        return self

    def update(self, payload):
        self.operation = "update"
        self.payload = payload
        return self

    def eq(self, key, value):
        self.filters[key] = value
        return self

    def maybe_single(self):
        return self

    def single(self):
        return self

    def order(self, *_args, **_kwargs):
        return self

    def limit(self, *_args, **_kwargs):
        return self

    def range(self, *_args, **_kwargs):
        return self

    def ilike(self, *_args, **_kwargs):
        return self

    def execute(self):
        key = (self.table_name, self.operation)
        data = self.db.responses.get(key, [])
        if callable(data):
            data = data(self)
        return SimpleNamespace(data=data)


class FakeDB:
    def __init__(self, responses):
        self.responses = responses
        self.auth = SimpleNamespace(
            sign_up=lambda *_args, **_kwargs: SimpleNamespace(
                user=SimpleNamespace(id="user-1")
            ),
            sign_in_with_password=lambda *_args, **_kwargs: SimpleNamespace(
                user=SimpleNamespace(id="user-1")
            ),
        )

    def table(self, table_name):
        return FakeQuery(self, table_name)


client = TestClient(app)


def test_register_success(monkeypatch):
    from app.api import auth

    monkeypatch.setattr(auth, "get_db", lambda: FakeDB({}))
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "student@example.com",
            "password": "securepassword",
            "full_name": "Student One",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["user_id"] == "user-1"
    assert body["access_token"]


def test_create_profile_success(monkeypatch):
    from app.api import students
    from app.core import dependencies

    profile_row = {
        "id": "profile-1",
        "full_name": "Student One",
        "class_level": 8,
        "board": "CBSE",
        "preferred_language": "English",
        "subjects": ["Mathematics"],
        "created_at": "2026-01-01T00:00:00Z",
    }
    fake_db = FakeDB(
        {
            ("student_profiles", "upsert"): [profile_row],
            ("student_progress", "upsert"): [{"student_id": "profile-1"}],
        }
    )
    monkeypatch.setattr(students, "get_db", lambda: fake_db)
    app.dependency_overrides[dependencies.get_current_user_id] = lambda: "user-1"

    response = client.post(
        "/api/v1/students/profile",
        json={
            "full_name": "Student One",
            "class_level": 8,
            "board": "CBSE",
            "preferred_language": "English",
            "subjects": ["Mathematics"],
        },
    )
    app.dependency_overrides.clear()
    assert response.status_code == 200
    body = response.json()
    assert body["profile_id"] == "profile-1"
    assert body["full_name"] == "Student One"


def test_progress_summary_success(monkeypatch):
    from app.api import progress
    from app.core import dependencies

    fake_db = FakeDB(
        {
            ("student_profiles", "select"): {"id": "profile-1", "full_name": "Student One"},
            ("student_progress", "select"): {
                "xp_total": 12,
                "xp_this_week": 12,
                "study_streak_days": 2,
                "subject_stats": {"Mathematics": {"sessions": 2, "xp": 12, "strength": "low"}},
                "weak_topics": [],
                "strong_topics": ["Integers"],
            },
            ("badge_awards", "select"): [{"badge_id": "first_session"}],
        }
    )
    monkeypatch.setattr(progress, "get_db", lambda: fake_db)
    app.dependency_overrides[dependencies.get_current_user_id] = lambda: "user-1"

    response = client.get("/api/v1/progress/summary")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    body = response.json()
    assert body["student_name"] == "Student One"
    assert body["badges"] == ["first_session"]
