"""
Pradyot AI — FastAPI Application Entry Point
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, chat, students, subjects, progress, pyq
from app.db.database import check_db_connection

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_db_ready_on_startup()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal mentor for Indian students (Class 1–10)",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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


def ensure_db_ready_on_startup() -> None:
    db_ok, _ = check_db_connection()
    if not db_ok:
        raise RuntimeError("Database connection failed during startup.")
    logger.info("Database connection verified at startup.")


# ─── HEALTH CHECK ────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    db_ok, _ = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "version": settings.APP_VERSION,
        "database": {
            "status": "ok" if db_ok else "error",
            "message": "ok" if db_ok else "connection unavailable",
        },
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Pradyot AI API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
