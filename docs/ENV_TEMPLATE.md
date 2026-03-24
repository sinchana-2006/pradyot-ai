# Pradyot AI — Environment Variables Template

This document lists all environment variables used in the project.  
**Never commit `.env` files to version control.** Use `.env.example` files as templates.

---

## Backend (`backend/.env`)

```env
# ─────────────────────────────────────────────
# APPLICATION
# ─────────────────────────────────────────────
APP_NAME=pradyot-ai
APP_ENV=development            # development | production
APP_VERSION=0.1.0
DEBUG=true                     # Set to false in production
SECRET_KEY=your-secret-key-min-32-chars-change-this-in-prod

# ─────────────────────────────────────────────
# SUPABASE (Database + Auth)
# Get from: Supabase Dashboard → Settings → API
# ─────────────────────────────────────────────
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-role-key   # Keep VERY secret

# ─────────────────────────────────────────────
# AI SERVICES
# ─────────────────────────────────────────────

# Groq API (Primary AI — Llama 3)
# Get from: https://console.groq.com → API Keys
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile    # Or llama-3.1-8b-instant for faster/cheaper

# Google Gemini (Fallback AI)
# Get from: https://aistudio.google.com → Get API Key
GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash         # Or gemini-1.5-pro for better quality

# ─────────────────────────────────────────────
# VOICE (Bhashini — Phase 2)
# Get from: https://bhashini.gov.in/ulca/search
# ─────────────────────────────────────────────
BHASHINI_API_KEY=your-bhashini-api-key
BHASHINI_USER_ID=your-bhashini-user-id
BHASHINI_PIPELINE_ID=your-bhashini-pipeline-id

# ─────────────────────────────────────────────
# CORS
# ─────────────────────────────────────────────
ALLOWED_ORIGINS=http://localhost:5173,https://pradyot-ai.vercel.app

# ─────────────────────────────────────────────
# RATE LIMITING
# ─────────────────────────────────────────────
RATE_LIMIT_CHAT=30/minute           # Chat messages per user
RATE_LIMIT_DEFAULT=120/minute       # Default for other endpoints

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
LOG_LEVEL=INFO                      # DEBUG | INFO | WARNING | ERROR
```

---

## Frontend (`frontend/.env`)

```env
# ─────────────────────────────────────────────
# API
# ─────────────────────────────────────────────
VITE_API_URL=http://localhost:8000                    # Backend API URL
VITE_API_VERSION=v1

# ─────────────────────────────────────────────
# SUPABASE (Public keys only — safe for frontend)
# Get from: Supabase Dashboard → Settings → API
# ─────────────────────────────────────────────
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key         # Anon key is safe for frontend

# ─────────────────────────────────────────────
# APP CONFIG
# ─────────────────────────────────────────────
VITE_APP_NAME=Pradyot AI
VITE_APP_ENV=development

# ─────────────────────────────────────────────
# FEATURE FLAGS
# ─────────────────────────────────────────────
VITE_ENABLE_VOICE=false            # Set to true when Bhashini is configured
VITE_ENABLE_PYQ=true
VITE_ENABLE_GAMIFICATION=true
```

---

## Variable Reference Table

| Variable | Required | Service | Notes |
|----------|----------|---------|-------|
| `SUPABASE_URL` | ✅ | Supabase | Project URL |
| `SUPABASE_ANON_KEY` | ✅ | Supabase | Safe for client-side |
| `SUPABASE_SERVICE_KEY` | ✅ | Supabase | **Backend only**, never expose |
| `GROQ_API_KEY` | ✅ | Groq | Primary AI service |
| `GEMINI_API_KEY` | ⚠️ | Google | Required for fallback |
| `BHASHINI_API_KEY` | 🔜 | Bhashini | Phase 2, voice features |
| `SECRET_KEY` | ✅ | App | JWT signing, min 32 chars |
| `ALLOWED_ORIGINS` | ✅ | App | Comma-separated CORS origins |

**Legend:** ✅ Required now | ⚠️ Recommended | 🔜 Future phase

---

## Security Notes

1. **Never commit `.env` files** — they are in `.gitignore`
2. **`SUPABASE_SERVICE_KEY`** is extremely sensitive — it bypasses all RLS policies. Keep it server-side only.
3. **`SECRET_KEY`** must be at least 32 random characters. Generate with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
4. **Frontend variables** with `VITE_` prefix are bundled into the client — **never put secrets in `VITE_` variables**
5. Use **Render's environment variables** dashboard for production backend secrets
6. Use **Vercel's environment variables** dashboard for production frontend variables

---

## Production Deployment Variables

### Vercel (Frontend)
Set these in Vercel dashboard → Project → Settings → Environment Variables:
- `VITE_API_URL` → Your Render backend URL
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

### Render (Backend)
Set these in Render dashboard → Service → Environment:
- All variables from `backend/.env`
- Set `APP_ENV=production` and `DEBUG=false`
