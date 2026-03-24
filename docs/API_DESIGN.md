# Pradyot AI — API Design

## Overview

All API routes are prefixed with `/api/v1/`. The backend is a FastAPI application with automatic OpenAPI documentation available at `/docs` (Swagger UI) and `/redoc`.

**Base URL (production):** `https://pradyot-ai-backend.onrender.com`  
**Base URL (local dev):** `http://localhost:8000`

---

## Authentication

All protected endpoints require a `Bearer` token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

Tokens are issued by Supabase Auth and validated by the FastAPI backend.

---

## Endpoints

### Auth

#### `POST /api/v1/auth/register`
Register a new user.

**Request:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123",
  "full_name": "Arjun Kumar"
}
```

**Response `201`:**
```json
{
  "user_id": "uuid-string",
  "email": "student@example.com",
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

**Errors:** `400` (email exists), `422` (validation error)

---

#### `POST /api/v1/auth/login`
Login with email and password.

**Request:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response `200`:**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user_id": "uuid-string"
}
```

**Errors:** `401` (invalid credentials)

---

### Student Profile

#### `POST /api/v1/students/profile`
Create or update the student's academic profile. 🔐 Auth required.

**Request:**
```json
{
  "full_name": "Arjun Kumar",
  "class_level": 8,
  "board": "CBSE",
  "preferred_language": "Hindi",
  "subjects": ["Mathematics", "Science", "English"]
}
```

**Response `200`:**
```json
{
  "profile_id": "uuid-string",
  "full_name": "Arjun Kumar",
  "class_level": 8,
  "board": "CBSE",
  "preferred_language": "Hindi",
  "subjects": ["Mathematics", "Science", "English"],
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

#### `GET /api/v1/students/profile`
Get the current student's profile. 🔐 Auth required.

**Response `200`:**
```json
{
  "profile_id": "uuid-string",
  "full_name": "Arjun Kumar",
  "class_level": 8,
  "board": "CBSE",
  "preferred_language": "Hindi",
  "subjects": ["Mathematics", "Science", "English"],
  "xp_total": 450,
  "badges": ["first_session", "7_day_streak"],
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### Chat

#### `POST /api/v1/chat/session`
Start a new chat session for a subject. 🔐 Auth required.

**Request:**
```json
{
  "subject": "Mathematics",
  "topic": "Quadratic Equations"
}
```

**Response `201`:**
```json
{
  "session_id": "uuid-string",
  "subject": "Mathematics",
  "topic": "Quadratic Equations",
  "started_at": "2024-01-01T10:00:00Z"
}
```

---

#### `POST /api/v1/chat/message`
Send a message and receive an AI response. 🔐 Auth required.

**Request:**
```json
{
  "session_id": "uuid-string",
  "message": "I don't understand how to solve x² + 5x + 6 = 0",
  "language": "Hindi"
}
```

**Response `200`:**
```json
{
  "response": "Great question, Arjun! Let's solve this step by step...",
  "follow_up_question": "Can you now try finding the factors of x² + 7x + 12?",
  "session_id": "uuid-string",
  "message_id": "uuid-string",
  "xp_earned": 5,
  "timestamp": "2024-01-01T10:05:00Z"
}
```

**Errors:** `404` (session not found), `429` (rate limit), `503` (AI service unavailable)

---

#### `GET /api/v1/chat/sessions`
Get the list of chat sessions for the current student. 🔐 Auth required.

**Query params:** `page` (int, default 1), `limit` (int, default 10), `subject` (string, optional)

**Response `200`:**
```json
{
  "sessions": [
    {
      "session_id": "uuid-string",
      "subject": "Mathematics",
      "topic": "Quadratic Equations",
      "message_count": 12,
      "xp_earned": 30,
      "started_at": "2024-01-01T10:00:00Z",
      "ended_at": "2024-01-01T10:45:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

---

#### `GET /api/v1/chat/session/{session_id}/messages`
Get all messages in a session. 🔐 Auth required.

**Response `200`:**
```json
{
  "session_id": "uuid-string",
  "messages": [
    {
      "message_id": "uuid-string",
      "role": "student",
      "content": "I don't understand quadratic equations",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    {
      "message_id": "uuid-string",
      "role": "assistant",
      "content": "Let me explain! A quadratic equation...",
      "timestamp": "2024-01-01T10:00:05Z"
    }
  ]
}
```

---

### Subjects

#### `GET /api/v1/subjects`
Get the list of available subjects for a class. 🔐 Auth required.

**Query params:** `class_level` (int, required), `board` (string, optional)

**Response `200`:**
```json
{
  "class_level": 8,
  "board": "CBSE",
  "subjects": [
    {
      "subject_id": "math",
      "name": "Mathematics",
      "topics": ["Linear Equations", "Quadratic Equations", "Geometry"]
    },
    {
      "subject_id": "science",
      "name": "Science",
      "topics": ["Force and Pressure", "Friction", "Sound"]
    }
  ]
}
```

---

### Progress

#### `GET /api/v1/progress/summary`
Get the student's progress summary. 🔐 Auth required.

**Response `200`:**
```json
{
  "student_name": "Arjun Kumar",
  "xp_total": 450,
  "xp_this_week": 120,
  "study_streak_days": 7,
  "badges": ["first_session", "7_day_streak", "math_explorer"],
  "subjects_covered": {
    "Mathematics": { "sessions": 5, "xp": 150, "strength": "medium" },
    "Science": { "sessions": 3, "xp": 90, "strength": "low" }
  },
  "weak_topics": ["Chemical Reactions", "Algebraic Identities"],
  "strong_topics": ["Triangles", "Integers"]
}
```

---

### PYQ (Previous Year Questions)

#### `GET /api/v1/pyq/questions`
Get previous year questions. 🔐 Auth required.

**Query params:** `subject` (string), `class_level` (int), `year` (int, optional), `chapter` (string, optional), `difficulty` (easy|medium|hard, optional), `limit` (int, default 10)

**Response `200`:**
```json
{
  "questions": [
    {
      "question_id": "uuid-string",
      "subject": "Mathematics",
      "class_level": 10,
      "year": 2023,
      "chapter": "Quadratic Equations",
      "question_text": "Find the roots of 2x² + 3x - 2 = 0",
      "marks": 3,
      "difficulty": "medium",
      "board": "CBSE"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 10
}
```

---

#### `POST /api/v1/pyq/check-answer`
Submit an answer to a PYQ and get AI feedback. 🔐 Auth required.

**Request:**
```json
{
  "question_id": "uuid-string",
  "student_answer": "x = 1/2 and x = -2",
  "session_id": "uuid-string"
}
```

**Response `200`:**
```json
{
  "is_correct": true,
  "feedback": "Excellent, Arjun! Your answer is correct. Both roots are x = 1/2 and x = -2.",
  "correct_answer": "x = 1/2 and x = -2",
  "explanation": "We use the factorization method...",
  "xp_earned": 10
}
```

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|-----------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request data |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Not allowed to access this resource |
| 404 | `NOT_FOUND` | Resource does not exist |
| 422 | `UNPROCESSABLE_ENTITY` | Request body schema mismatch |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 503 | `AI_SERVICE_UNAVAILABLE` | Groq and Gemini both unavailable |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `POST /chat/message` | 30 requests/minute per user |
| `POST /pyq/check-answer` | 60 requests/minute per user |
| All other endpoints | 120 requests/minute per user |

---

## Versioning

API versioning is done via URL path (`/api/v1/`). Breaking changes will increment the version number. The old version will be supported for at least 6 months after deprecation notice.
