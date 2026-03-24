-- Migration 002: Seed Badge Definitions
-- Run after 001_initial_schema.sql

INSERT INTO badges (id, name, description, xp_reward, criteria_type, criteria_value) VALUES
    ('first_session',  'First Step',        'Completed your first learning session',    50,  'sessions',        1),
    ('sessions_5',     'Getting Started',   'Completed 5 learning sessions',            75,  'sessions',        5),
    ('sessions_25',    'Learning Machine',  'Completed 25 learning sessions',          200,  'sessions',        25),
    ('streak_3',       '3-Day Streak',      'Studied 3 days in a row',                  50,  'streak',          3),
    ('streak_7',       'Week Warrior',      'Studied 7 days in a row',                 150,  'streak',          7),
    ('streak_30',      'Monthly Master',    'Studied 30 days in a row',                500,  'streak',          30),
    ('pyq_first',      'PYQ Pioneer',       'Solved your first previous year question',  75,  'pyq_solved',      1),
    ('pyq_10',         'Exam Ready',        'Solved 10 previous year questions',        200,  'pyq_solved',      10),
    ('math_explorer',  'Math Explorer',     'Had 5+ Math sessions',                    100,  'subject_sessions', 5),
    ('science_star',   'Science Star',      'Had 5+ Science sessions',                 100,  'subject_sessions', 5),
    ('english_ace',    'English Ace',       'Had 5+ English sessions',                 100,  'subject_sessions', 5)
ON CONFLICT (id) DO NOTHING;
