# PradyotAI

AI-powered personal mentor for Indian school students (Class 1–10). Making quality education accessible, personalized, and fun — especially for kids in rural India.

**Tech Stack:** FastAPI • React • Google Gemini • Supabase

## Quick Start

### 1. Environment Setup

```bash
# Copy and fill in your credentials (from project root)
cp .env.example .env
# Edit .env with: GEMINI_API_KEY, SUPABASE_URL, SUPABASE_ANON_KEY
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend

```bash
cd frontend
cp .env.example .env    # Optional: VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

Open http://localhost:5173 — onboard as a student, then chat with PradyotAI!
