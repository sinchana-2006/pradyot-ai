# Pradyot AI — Database Schema

## Overview

Pradyot AI uses **Supabase (PostgreSQL)** as the primary database. Supabase handles authentication, Row Level Security (RLS), and real-time capabilities.

---

## Entity Relationship Diagram (Text)

```
users (Supabase Auth)
  │
  └──< student_profiles (1:1 per user)
           │
           ├──< chat_sessions (1:many)
           │         │
           │         └──< messages (1:many)
           │
           ├──< student_progress (1:1)
           │         │
           │         └──< badge_awards (1:many)
           │
           └──< pyq_attempts (1:many)
                     │
                     └──> pyq_questions (many:1, shared bank)
```

---

## DDL — Full Schema

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─────────────────────────────────────────────
-- STUDENT PROFILES
-- ─────────────────────────────────────────────
CREATE TABLE student_profiles (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name           VARCHAR(100) NOT NULL,
    class_level         SMALLINT NOT NULL CHECK (class_level BETWEEN 1 AND 10),
    board               VARCHAR(20) NOT NULL CHECK (board IN ('CBSE', 'ICSE', 'State Board', 'Other')),
    state               VARCHAR(50),                    -- For State Board students
    preferred_language  VARCHAR(30) NOT NULL DEFAULT 'English',
    subjects            TEXT[] NOT NULL DEFAULT '{}',   -- Array of active subjects
    avatar_url          TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id)
);

-- ─────────────────────────────────────────────
-- CHAT SESSIONS
-- ─────────────────────────────────────────────
CREATE TABLE chat_sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    subject         VARCHAR(50) NOT NULL,
    topic           VARCHAR(100),
    status          VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'ended')),
    xp_earned       INTEGER NOT NULL DEFAULT 0,
    message_count   INTEGER NOT NULL DEFAULT 0,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at        TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}'     -- Extensible: difficulty, confusion_flags, etc.
);

-- ─────────────────────────────────────────────
-- MESSAGES
-- ─────────────────────────────────────────────
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role            VARCHAR(20) NOT NULL CHECK (role IN ('student', 'assistant', 'system')),
    content         TEXT NOT NULL,
    language        VARCHAR(30),               -- Language used in this message
    tokens_used     INTEGER,                   -- For cost tracking
    xp_awarded      INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- STUDENT PROGRESS
-- ─────────────────────────────────────────────
CREATE TABLE student_progress (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id          UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    xp_total            INTEGER NOT NULL DEFAULT 0,
    xp_this_week        INTEGER NOT NULL DEFAULT 0,
    study_streak_days   INTEGER NOT NULL DEFAULT 0,
    last_active_date    DATE,
    subject_stats       JSONB NOT NULL DEFAULT '{}',  -- Per-subject XP, session count, strength
    weak_topics         TEXT[] DEFAULT '{}',
    strong_topics       TEXT[] DEFAULT '{}',
    total_sessions      INTEGER NOT NULL DEFAULT 0,
    total_messages      INTEGER NOT NULL DEFAULT 0,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(student_id)
);

-- ─────────────────────────────────────────────
-- BADGES
-- ─────────────────────────────────────────────
CREATE TABLE badges (
    id              VARCHAR(50) PRIMARY KEY,   -- e.g., 'first_session', '7_day_streak'
    name            VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    icon_url        TEXT,
    xp_reward       INTEGER NOT NULL DEFAULT 0,
    criteria_type   VARCHAR(50) NOT NULL,      -- 'sessions', 'streak', 'pyq_solved', etc.
    criteria_value  INTEGER NOT NULL           -- Threshold value for the badge
);

CREATE TABLE badge_awards (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    badge_id        VARCHAR(50) NOT NULL REFERENCES badges(id),
    awarded_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(student_id, badge_id)
);

-- ─────────────────────────────────────────────
-- PYQ (PREVIOUS YEAR QUESTIONS)
-- ─────────────────────────────────────────────
CREATE TABLE pyq_questions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    board           VARCHAR(20) NOT NULL CHECK (board IN ('CBSE', 'ICSE', 'State Board')),
    class_level     SMALLINT NOT NULL CHECK (class_level BETWEEN 1 AND 10),
    subject         VARCHAR(50) NOT NULL,
    chapter         VARCHAR(100),
    year            SMALLINT,
    question_text   TEXT NOT NULL,
    marks           SMALLINT,
    difficulty      VARCHAR(10) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    answer_key      TEXT,                     -- Official answer / solution steps
    tags            TEXT[] DEFAULT '{}',
    source_url      TEXT,                     -- Link to official paper if available
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE pyq_attempts (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id          UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    question_id         UUID NOT NULL REFERENCES pyq_questions(id),
    session_id          UUID REFERENCES chat_sessions(id),
    student_answer      TEXT NOT NULL,
    is_correct          BOOLEAN,
    ai_feedback         TEXT,
    xp_awarded          INTEGER NOT NULL DEFAULT 0,
    attempted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- INDEXES
-- ─────────────────────────────────────────────
CREATE INDEX idx_chat_sessions_student ON chat_sessions(student_id);
CREATE INDEX idx_chat_sessions_status  ON chat_sessions(status);
CREATE INDEX idx_messages_session      ON messages(session_id);
CREATE INDEX idx_messages_created      ON messages(created_at);
CREATE INDEX idx_pyq_questions_board_class ON pyq_questions(board, class_level, subject);
CREATE INDEX idx_pyq_attempts_student  ON pyq_attempts(student_id);
CREATE INDEX idx_badge_awards_student  ON badge_awards(student_id);

-- ─────────────────────────────────────────────
-- ROW LEVEL SECURITY (RLS)
-- ─────────────────────────────────────────────
ALTER TABLE student_profiles  ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions      ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages           ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_progress   ENABLE ROW LEVEL SECURITY;
ALTER TABLE badge_awards       ENABLE ROW LEVEL SECURITY;
ALTER TABLE pyq_attempts       ENABLE ROW LEVEL SECURITY;

-- Student profiles: users can only see/edit their own profile
CREATE POLICY "Students own their profile"
    ON student_profiles FOR ALL
    USING (auth.uid() = user_id);

-- Chat sessions: students can only access their own sessions
CREATE POLICY "Students own their sessions"
    ON chat_sessions FOR ALL
    USING (student_id IN (
        SELECT id FROM student_profiles WHERE user_id = auth.uid()
    ));

-- Messages: students can only see messages in their own sessions
CREATE POLICY "Students own their messages"
    ON messages FOR ALL
    USING (session_id IN (
        SELECT cs.id FROM chat_sessions cs
        JOIN student_profiles sp ON cs.student_id = sp.id
        WHERE sp.user_id = auth.uid()
    ));

-- Progress: students own their progress records
CREATE POLICY "Students own their progress"
    ON student_progress FOR ALL
    USING (student_id IN (
        SELECT id FROM student_profiles WHERE user_id = auth.uid()
    ));

-- PYQ questions are public read
CREATE POLICY "PYQ questions are public"
    ON pyq_questions FOR SELECT
    USING (true);

-- ─────────────────────────────────────────────
-- SEED DATA — BADGES
-- ─────────────────────────────────────────────
INSERT INTO badges (id, name, description, xp_reward, criteria_type, criteria_value) VALUES
    ('first_session',  'First Step',        'Completed your first learning session',   50,  'sessions', 1),
    ('sessions_5',     'Getting Started',   'Completed 5 learning sessions',           75,  'sessions', 5),
    ('sessions_25',    'Learning Machine',  'Completed 25 learning sessions',         200,  'sessions', 25),
    ('streak_3',       '3-Day Streak',      'Studied 3 days in a row',                 50,  'streak',   3),
    ('streak_7',       'Week Warrior',      'Studied 7 days in a row',                150,  'streak',   7),
    ('streak_30',      'Monthly Master',    'Studied 30 days in a row',               500,  'streak',   30),
    ('pyq_first',      'PYQ Pioneer',       'Solved your first previous year question', 75, 'pyq_solved', 1),
    ('pyq_10',         'Exam Ready',        'Solved 10 previous year questions',      200,  'pyq_solved', 10),
    ('math_explorer',  'Math Explorer',     'Had 5+ Math sessions',                   100,  'subject_sessions', 5),
    ('science_star',   'Science Star',      'Had 5+ Science sessions',                100,  'subject_sessions', 5);
```

---

## subject_stats JSON Structure

The `subject_stats` column in `student_progress` uses this structure:

```json
{
  "Mathematics": {
    "sessions": 5,
    "xp": 150,
    "strength": "medium",
    "last_session": "2024-01-15T10:30:00Z",
    "weak_topics": ["Quadratic Equations"],
    "strong_topics": ["Triangles", "Integers"]
  },
  "Science": {
    "sessions": 3,
    "xp": 90,
    "strength": "low",
    "last_session": "2024-01-14T09:00:00Z",
    "weak_topics": ["Chemical Reactions"],
    "strong_topics": []
  }
}
```

---

## Migrations

Migration files are stored in `/database/migrations/` and are numbered sequentially:

```
database/migrations/
├── 001_initial_schema.sql      — All tables, indexes, RLS
├── 002_seed_badges.sql         — Badge definitions
└── 003_seed_pyq_class10.sql    — CBSE Class 10 PYQ data (Phase 1)
```

---

## Notes

- All timestamps are stored in UTC (`TIMESTAMPTZ`)
- UUIDs used for all primary keys (distributed-safe)
- RLS ensures users cannot access other students' data
- `metadata` and `subject_stats` use JSONB for extensibility without schema migrations
- `pyq_questions.answer_key` is server-side only and never sent to frontend directly
