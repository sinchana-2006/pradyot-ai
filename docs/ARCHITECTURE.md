# Pradyot AI — System Architecture

## Overview

Pradyot AI is a **full-stack AI tutoring platform** built with a React frontend, FastAPI backend, Supabase database, and multiple AI/voice APIs. The architecture is designed to be lightweight, scalable, and accessible on low-bandwidth connections.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
│                                                             │
│   ┌──────────────────────────────────────────────────────┐  │
│   │           React (Vite) Frontend — Vercel             │  │
│   │  • Student chat interface                            │  │
│   │  • Onboarding profile form                          │  │
│   │  • Progress dashboard                               │  │
│   │  • Voice I/O controls                               │  │
│   └────────────────────────┬─────────────────────────────┘  │
│                            │ HTTPS / REST API                │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                       API LAYER                             │
│                                                             │
│   ┌──────────────────────────────────────────────────────┐  │
│   │              FastAPI Backend — Render                │  │
│   │                                                      │  │
│   │  ┌──────────────┐  ┌──────────────┐                 │  │
│   │  │  /auth       │  │  /students   │                 │  │
│   │  │  /chat       │  │  /progress   │                 │  │
│   │  │  /subjects   │  │  /pyq        │                 │  │
│   │  └──────────────┘  └──────────────┘                 │  │
│   │                                                      │  │
│   │  ┌─────────────────────────────────────────────┐    │  │
│   │  │              Service Layer                  │    │  │
│   │  │  • AI Service (Groq → Gemini fallback)      │    │  │
│   │  │  • Voice Service (Bhashini API)             │    │  │
│   │  │  • Session Manager                          │    │  │
│   │  │  • Gamification Engine                      │    │  │
│   │  └─────────────────────────────────────────────┘    │  │
│   └──────────────────────────────────────────────────────┘  │
└──────────────┬───────────────────────────┬──────────────────┘
               │                           │
┌──────────────▼───────┐   ┌───────────────▼──────────────────┐
│   DATA LAYER         │   │       EXTERNAL APIS              │
│                      │   │                                  │
│  ┌─────────────────┐ │   │  ┌────────────┐ ┌────────────┐  │
│  │  Supabase       │ │   │  │  Groq API  │ │  Gemini    │  │
│  │  PostgreSQL     │ │   │  │  (Llama 3) │ │  (Fallback)│  │
│  │                 │ │   │  └────────────┘ └────────────┘  │
│  │  • users        │ │   │                                  │
│  │  • students     │ │   │  ┌────────────────────────────┐  │
│  │  • sessions     │ │   │  │      Bhashini API          │  │
│  │  • messages     │ │   │  │  (Indian Voice & Language) │  │
│  │  • progress     │ │   │  └────────────────────────────┘  │
│  │  • pyq_bank     │ │   │                                  │
│  └─────────────────┘ │   └──────────────────────────────────┘
└──────────────────────┘
```

---

## Component Breakdown

### Frontend (React + Vite)

| Component | Responsibility |
|-----------|----------------|
| `ChatInterface` | Main chat UI, message bubbles, input box |
| `OnboardingForm` | Student profile creation (class, board, language) |
| `SubjectSelector` | Choose subject for current session |
| `ProgressDashboard` | XP, badges, study streak display |
| `VoiceControls` | Mic input and TTS output toggle |
| `PYQPractice` | Previous year question browser |

**State Management:** Zustand (lightweight, no Redux boilerplate)  
**Routing:** React Router v6  
**Styling:** Tailwind CSS  
**HTTP Client:** Axios  

### Backend (FastAPI)

| Module | Responsibility |
|--------|----------------|
| `api/auth.py` | User registration, login, JWT token management |
| `api/chat.py` | Chat endpoint, conversation handling |
| `api/students.py` | Student profile CRUD |
| `api/subjects.py` | Subject and topic listing |
| `api/progress.py` | XP, badges, session history |
| `api/pyq.py` | Previous year question retrieval |
| `services/ai_service.py` | Groq/Gemini integration and prompt management |
| `services/voice_service.py` | Bhashini API integration |
| `services/session_service.py` | Conversation context management |
| `core/config.py` | Environment variables and settings |
| `core/security.py` | JWT creation, password hashing |
| `db/database.py` | Supabase connection and query helpers |

### Database (Supabase PostgreSQL)

Core tables:
- `users` — Authentication records
- `student_profiles` — Academic profile (class, board, language)
- `chat_sessions` — Conversation sessions
- `messages` — Individual messages in a session
- `student_progress` — XP, badges, subject strengths
- `pyq_bank` — Previous year questions database

See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for full schema.

---

## Request Flow — Chat Message

```
Student types message
        │
        ▼
React Frontend
  • Appends message to local state
  • POST /api/v1/chat/message
        │
        ▼
FastAPI /chat endpoint
  • Validates JWT token
  • Loads student profile (class, board, language, weak areas)
  • Loads last N messages from session (context window)
        │
        ▼
AI Service (ai_service.py)
  • Builds system prompt with student context
  • Calls Groq API (Llama 3.3 70B)
  • Falls back to Gemini if Groq fails
  • Returns structured response
        │
        ▼
Session Service
  • Saves student message + AI response to Supabase
  • Updates session metadata
  • Calculates XP if applicable
        │
        ▼
FastAPI response
  • Returns AI message text
  • Returns XP delta (if any)
  • Returns follow-up question
        │
        ▼
React Frontend
  • Renders AI response in chat bubble
  • Updates XP counter if applicable
  • Triggers TTS via Bhashini (if voice mode on)
```

---

## AI Prompt Architecture

### System Prompt Variables
```
{student_name}      — Student's first name
{class_level}       — Class 1–10
{board}             — CBSE / ICSE / State Board
{language}          — Preferred language
{subject}           — Current subject
{weak_topics}       — Known weak areas from history
{session_context}   — Last N messages for context
```

### Prompt Strategy
1. **Persona**: Friendly, patient Indian mentor (not formal teacher)
2. **Language**: Match student's preferred language; use simple vocabulary for lower classes
3. **Examples**: Use Indian cultural references (cricket, chai, festivals)
4. **Socratic**: Guide to answer with questions, don't just give answers
5. **Brevity**: Short paragraphs, bullet points for steps
6. **Follow-up**: Always end with a comprehension check question
7. **Emotion**: Detect frustration, respond with encouragement

### Fallback Chain
```
Groq (Llama 3.3 70B) → Gemini 1.5 Flash → Error with helpful message
```

---

## Voice Architecture (Phase 2)

```
User speech
    │
    ▼ Bhashini ASR (Automatic Speech Recognition)
    │ Converts regional language audio → text
    ▼
FastAPI Chat endpoint
    │ Processes as normal text message
    ▼
Bhashini TTS (Text-to-Speech)
    │ Converts AI response text → regional language audio
    ▼
Frontend audio player
```

**Supported Languages (Phase 2):** Hindi, Kannada, Tamil, Telugu, Marathi, Bengali, Gujarati, Odia, Punjabi, Malayalam

---

## Security Design

| Concern | Approach |
|---------|----------|
| Authentication | Supabase Auth + JWT tokens |
| API authorization | JWT verified on every protected endpoint |
| API keys | Environment variables only, never in code |
| Student data | Supabase Row Level Security (RLS) policies |
| CORS | Restricted to frontend domain in production |
| Rate limiting | FastAPI middleware (slowapi) |
| Input validation | Pydantic models on all endpoints |

---

## Scalability Considerations

- **Stateless backend** — All session state stored in DB, backend can scale horizontally
- **Connection pooling** — Supabase manages PostgreSQL connections
- **Edge caching** — Vercel CDN for static assets
- **AI latency** — Streaming responses (future) for better UX on slow connections
- **Low-bandwidth mode** — Text-only UI option, minimal assets

---

## Phase Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 0 | Foundation setup, documentation | ✅ In Progress |
| Phase 1 | MVP chat, English/Hindi, CBSE Class 10 | 🔜 Planned |
| Phase 2 | Voice, regional languages, PWA, parent dashboard | 🔜 Planned |
| Phase 3 | WhatsApp bot, school admin, CSR portal | 🔜 Planned |
