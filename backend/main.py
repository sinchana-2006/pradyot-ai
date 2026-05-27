"""
Pradyot AI — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, chat, students, subjects, progress, pyq
from app.db.database import check_db_connection

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal mentor for Indian students (Class 1–10)",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ─────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth.router,      prefix=f"{API_PREFIX}/auth",     tags=["Auth"])
app.include_router(students.router,  prefix=f"{API_PREFIX}/students",  tags=["Students"])
app.include_router(chat.router,      prefix=f"{API_PREFIX}/chat",      tags=["Chat"])
app.include_router(subjects.router,  prefix=f"{API_PREFIX}/subjects",  tags=["Subjects"])
app.include_router(progress.router,  prefix=f"{API_PREFIX}/progress",  tags=["Progress"])
app.include_router(pyq.router,       prefix=f"{API_PREFIX}/pyq",       tags=["PYQ"])


# ─── HEALTH CHECK ────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    db_ok, db_message = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "version": settings.APP_VERSION,
        "database": {
            "status": "ok" if db_ok else "error",
            "message": db_message,
        },
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Pradyot AI API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
