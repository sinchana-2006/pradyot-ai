# Pradyot AI — Local Development Setup Guide

## Prerequisites

Make sure the following tools are installed before you begin:

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| npm | 9+ | Included with Node.js |
| Git | 2.x | [git-scm.com](https://git-scm.com) |
| Docker (optional) | 24+ | [docker.com](https://docker.com) |

---

## 1. Clone the Repository

```bash
git clone https://github.com/sinchana-2006/pradyot-ai.git
cd pradyot-ai
```

---

## 2. Create External Accounts & Get API Keys

You'll need free accounts with these services:

### Supabase (Database + Auth)
1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to **Settings → API** and copy:
   - `Project URL` → `SUPABASE_URL`
   - `anon/public` key → `SUPABASE_ANON_KEY`
   - `service_role` key → `SUPABASE_SERVICE_KEY` (keep secret!)
4. Go to **SQL Editor** and run the schema from `/database/migrations/001_initial_schema.sql`

### Groq API (Primary AI)
1. Go to [console.groq.com](https://console.groq.com) and sign up (free tier available)
2. Create an API key → `GROQ_API_KEY`

### Google Gemini API (Fallback AI)
1. Go to [aistudio.google.com](https://aistudio.google.com) and sign in
2. Create an API key → `GEMINI_API_KEY`

### Bhashini API (Voice — Phase 2)
1. Go to [bhashini.gov.in](https://bhashini.gov.in) and register
2. Get your API key → `BHASHINI_API_KEY`

---

## 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows (Command Prompt):
venv\Scripts\activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

Now edit `backend/.env` with your actual API keys (see [ENV_TEMPLATE.md](ENV_TEMPLATE.md)):

```bash
# Start the backend development server
uvicorn main:app --reload --port 8000
```

The backend will be available at:
- **API:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 4. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
```

Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

```bash
# Start the frontend development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 5. Database Setup

Run the migration files in order against your Supabase project:

### Via Supabase SQL Editor
1. Open your Supabase project
2. Go to **SQL Editor → New Query**
3. Copy and paste each migration file in order:
   ```
   database/migrations/001_initial_schema.sql
   database/migrations/002_seed_badges.sql
   ```
4. Run each file

### Via Supabase CLI (recommended)
```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link to your project
supabase link --project-ref your_project_ref

# Run migrations
supabase db push
```

---

## 6. Verify Setup

Check that everything is running correctly:

```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
# {"status": "ok", "version": "0.1.0"}
```

Visit `http://localhost:5173` — you should see the Pradyot AI home page.

---

## 7. Docker Setup (Optional)

If you prefer to use Docker:

```bash
# From the root of the repository
docker-compose up --build

# This starts:
# - Backend at http://localhost:8000
# - Frontend at http://localhost:5173
```

Stop containers:
```bash
docker-compose down
```

---

## Troubleshooting

### Backend won't start
```
Error: ModuleNotFoundError
```
Make sure your virtual environment is activated and run `pip install -r requirements.txt` again.

### Frontend can't connect to backend
Check that:
1. Backend is running at `http://localhost:8000`
2. `VITE_API_URL` in `frontend/.env` is set to `http://localhost:8000`
3. No CORS errors in the browser console

### Supabase connection fails
Check that:
1. `SUPABASE_URL` and `SUPABASE_ANON_KEY` are correct in `backend/.env`
2. Your Supabase project is active (not paused — free tier pauses after 7 days of inactivity)

### Groq API errors
Check that `GROQ_API_KEY` is valid at [console.groq.com](https://console.groq.com)

---

## Project Scripts Reference

### Backend
```bash
uvicorn main:app --reload        # Dev server with hot reload
pytest                           # Run tests
python -m pytest -v              # Run tests with verbose output
```

### Frontend
```bash
npm run dev          # Dev server
npm run build        # Production build
npm run preview      # Preview production build
npm run lint         # ESLint
```

---

## Directory Structure Reference

```
pradyot-ai/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI route handlers
│   │   ├── core/           # Config, security
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # AI, voice, session logic
│   │   └── db/             # DB connection and queries
│   ├── main.py             # FastAPI app entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Route pages
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API client
│   │   ├── store/          # Zustand state
│   │   └── utils/          # Helpers
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── database/
│   ├── schema.sql          # Full schema reference
│   └── migrations/         # Numbered migration files
└── docs/                   # All documentation
```
