-- Pradyot AI — Full Database Schema (Reference)
-- This file is the canonical schema reference.
-- For migration-based setup, use the files in /database/migrations/

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
    state               VARCHAR(50),
    preferred_language  VARCHAR(30) NOT NULL DEFAULT 'English',
    subjects            TEXT[] NOT NULL DEFAULT '{}',
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
    metadata        JSONB DEFAULT '{}'
);

-- ─────────────────────────────────────────────
-- MESSAGES
-- ─────────────────────────────────────────────
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role            VARCHAR(20) NOT NULL CHECK (role IN ('student', 'assistant', 'system')),
    content         TEXT NOT NULL,
    language        VARCHAR(30),
    tokens_used     INTEGER,
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
    subject_stats       JSONB NOT NULL DEFAULT '{}',
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
    id              VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    icon_url        TEXT,
    xp_reward       INTEGER NOT NULL DEFAULT 0,
    criteria_type   VARCHAR(50) NOT NULL,
    criteria_value  INTEGER NOT NULL
);

CREATE TABLE badge_awards (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    badge_id        VARCHAR(50) NOT NULL REFERENCES badges(id),
    awarded_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(student_id, badge_id)
);

-- ─────────────────────────────────────────────
-- PYQ QUESTIONS
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
    answer_key      TEXT,
    tags            TEXT[] DEFAULT '{}',
    source_url      TEXT,
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
CREATE INDEX idx_chat_sessions_student     ON chat_sessions(student_id);
CREATE INDEX idx_chat_sessions_status      ON chat_sessions(status);
CREATE INDEX idx_messages_session          ON messages(session_id);
CREATE INDEX idx_messages_created          ON messages(created_at);
CREATE INDEX idx_pyq_questions_board_class ON pyq_questions(board, class_level, subject);
CREATE INDEX idx_pyq_attempts_student      ON pyq_attempts(student_id);
CREATE INDEX idx_badge_awards_student      ON badge_awards(student_id);

-- ─────────────────────────────────────────────
-- ROW LEVEL SECURITY (RLS)
-- ─────────────────────────────────────────────
ALTER TABLE student_profiles  ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions      ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages           ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_progress   ENABLE ROW LEVEL SECURITY;
ALTER TABLE badge_awards       ENABLE ROW LEVEL SECURITY;
ALTER TABLE pyq_attempts       ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Students own their profile"
    ON student_profiles FOR ALL
    USING (auth.uid() = user_id);

CREATE POLICY "Students own their sessions"
    ON chat_sessions FOR ALL
    USING (student_id IN (
        SELECT id FROM student_profiles WHERE user_id = auth.uid()
    ));

CREATE POLICY "Students own their messages"
    ON messages FOR ALL
    USING (session_id IN (
        SELECT cs.id FROM chat_sessions cs
        JOIN student_profiles sp ON cs.student_id = sp.id
        WHERE sp.user_id = auth.uid()
    ));

CREATE POLICY "Students own their progress"
    ON student_progress FOR ALL
    USING (student_id IN (
        SELECT id FROM student_profiles WHERE user_id = auth.uid()
    ));

CREATE POLICY "PYQ questions are public"
    ON pyq_questions FOR SELECT
    USING (true);
