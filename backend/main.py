"""
PradyotAI - FastAPI Backend Entry Point
AI-powered personal mentor for Indian school students (Class 1-10).
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv

from app.models import ChatRequest, ChatResponse, StudentOnboarding
from app.chat import get_chat_response
from app.database import get_supabase_client

# Load .env from project root (pradyot-ai/.env)
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")

app = FastAPI(
    title="PradyotAI API",
    description="AI-powered personal tutor for Indian school students",
    version="1.0.0",
)

# CORS - Allow frontend (React) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "PradyotAI API is running", "status": "ok"}


@app.get("/health")
async def health():
    """Health check for deployment monitoring."""
    return {"status": "healthy"}


@app.post("/api/onboard", response_model=dict)
async def onboard_student(student: StudentOnboarding):
    """
    Save student onboarding data to Supabase.
    Returns student_id for use in chat.
    """
    try:
        supabase = get_supabase_client()
        result = supabase.table("students").insert({
            "name": student.name,
            "class": student.class_level,
            "board": student.board,
            "language": student.preferred_language,
        }).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to create student record",
            )

        student_record = result.data[0]
        student_id = student_record["id"]

        student_data = student.model_dump()
        student_data["id"] = student_id

        return {
            "success": True,
            "message": f"Welcome, {student.name}! Ready to learn {student.subject}.",
            "student": student_data,
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save student: {str(e)}",
        )


def _save_chat_message(student_id: str, subject: str, role: str, message: str) -> None:
    """Save a single message to chat_history. Logs but does not raise on error."""
    try:
        supabase = get_supabase_client()
        supabase.table("chat_history").insert({
            "student_id": student_id,
            "subject": subject,
            "role": role,
            "message": message,
        }).execute()
    except Exception as e:
        logging.warning(f"Failed to save chat message to Supabase: {e}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to PradyotAI and get a response.
    Saves both user and AI messages to chat_history when student_id is provided.
    """
    try:
        response_text = get_chat_response(
            message=request.message,
            student_context=request.student_context,
            history=request.history,
        )

        # Save to chat_history if we have student_id and subject
        if request.student_id and request.student_context:
            subject = request.student_context.subject
            _save_chat_message(
                student_id=request.student_id,
                subject=subject,
                role="user",
                message=request.message,
            )
            _save_chat_message(
                student_id=request.student_id,
                subject=subject,
                role="assistant",
                message=response_text,
            )

        return ChatResponse(message=response_text, success=True)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get AI response: {str(e)}",
        )
