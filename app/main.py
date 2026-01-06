"""
WDC Labs AI Backend
FastAPI application for the immersive virtual office AI system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import os

from .schemas import (
    ChatRequest, ChatResponse,
    BioAssessmentRequest, BioAssessmentResponse,
    SubmissionReviewRequest, SubmissionReviewResponse,
    PortfolioBulletRequest, PortfolioBulletResponse
)
from .orchestrator import Orchestrator

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize orchestrator
orchestrator = Orchestrator(model)

# Create FastAPI app
app = FastAPI(
    title="WDC Labs AI Backend",
    description="Immersive Virtual Office AI System with Multi-Agent Architecture",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "WDC Labs AI Backend is running"}


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "model": "gemini-2.5-flash",
        "agents": ["Tolu", "Emem", "Sola", "Kemi"]
    }


# ============ CHAT ENDPOINTS ============

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - routes messages to appropriate agent.
    
    The orchestrator determines which agent should respond based on:
    - Message content (keywords)
    - Context (is_submission, is_first_login, etc.)
    """
    try:
        response = await orchestrator.route_message(
            message=request.message,
            context=request.context,
            chat_history=request.chat_history or []
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ ONBOARDING ENDPOINTS ============

@app.post("/assess-bio", response_model=BioAssessmentResponse)
async def assess_bio(request: BioAssessmentRequest):
    """
    Tolu assesses the user's bio/resume and assigns a skill level.
    
    Returns:
    - Level 0 (Foundation): No computer skills, digital literacy focus
    - Level 1 (Beginner): Some education, no real experience
    - Level 2 (Intermediate): Has degree or specific technical skills
    """
    try:
        bio_text = request.bio_text or ""
        
        # If file_url is provided, we'd need to fetch and extract text
        # For now, we work with bio_text
        if not bio_text and not request.file_url:
            raise HTTPException(
                status_code=400, 
                detail="Either bio_text or file_url must be provided"
            )
        
        result = await orchestrator.assess_bio(bio_text, request.track)
        
        return BioAssessmentResponse(
            response_text=result.get("response_text", "Welcome to WDC Labs."),
            assessed_level=result.get("assessed_level", "Level 1"),
            reasoning=result.get("reasoning", "Assessment completed."),
            warmup_mode=result.get("warmup_mode", False)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ SUBMISSION ENDPOINTS ============

@app.post("/review-submission", response_model=SubmissionReviewResponse)
async def review_submission(request: SubmissionReviewRequest):
    """
    Sola reviews a user's work submission.
    
    Implements the 60% Rejection Rule - only truly excellent work passes.
    If passed, Kemi automatically generates a CV bullet point.
    """
    try:
        submission_content = request.file_content or f"[File submitted: {request.file_url}]"
        
        result = await orchestrator.review_submission(
            task_title=request.task_title,
            task_brief=request.task_brief,
            submission_content=submission_content,
            client_constraints=None
        )
        
        portfolio_bullet = None
        if result.get("passed") and result.get("portfolio_bullet"):
            portfolio_bullet = result["portfolio_bullet"].get("bullet_point")
        
        return SubmissionReviewResponse(
            feedback=result.get("feedback", "Review completed."),
            passed=result.get("passed", False),
            score=result.get("score"),
            portfolio_bullet=portfolio_bullet
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interrogate-submission")
async def interrogate_submission(submission_content: str, approach: str):
    """
    Sola's Socratic Defense - interrogate a user about their choices.
    
    Used to detect copied/AI-generated work by asking about specific decisions.
    """
    try:
        questions = await orchestrator.interrogate_submission(
            submission_content=submission_content,
            approach_used=approach
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ PORTFOLIO ENDPOINTS ============

@app.post("/translate-to-cv", response_model=PortfolioBulletResponse)
async def translate_to_cv(request: PortfolioBulletRequest):
    """
    Kemi translates a completed task into a CV bullet point.
    """
    try:
        from .agents import kemi
        result = await kemi.translate_to_cv_bullet(
            task_title=request.task_title,
            task_description=request.task_description,
            user_accomplishment=request.user_submission,
            model=model
        )
        return PortfolioBulletResponse(
            skill_tag=result.get("skill_tag", "General"),
            bullet_point=result.get("bullet_point", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ INTERRUPTION ENDPOINTS ============

@app.post("/generate-interruption")
async def generate_interruption(current_task: str, interruption_type: str = "scope_change"):
    """
    Generate a mid-task client interruption (The "Moving Target").
    
    Types: scope_change, constraint_added, urgent_pivot, data_correction
    """
    try:
        interruption = await orchestrator.generate_client_interruption(
            current_task=current_task,
            interruption_type=interruption_type
        )
        return {"agent": "Emem", "message": interruption}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ COACHING ENDPOINTS ============

@app.post("/soft-skills-feedback")
async def get_soft_skills_feedback(recent_interactions: list):
    """
    Kemi analyzes recent interactions and provides soft skills feedback.
    """
    try:
        feedback = await orchestrator.get_soft_skills_feedback(recent_interactions)
        return {"agent": "Kemi", "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mock-interview")
async def mock_interview(
    interview_type: str = "behavioral",
    question_number: int = 1,
    previous_answer: str = None
):
    """
    Conduct a mock interview session with Kemi.
    
    Types: behavioral, technical, situational
    """
    try:
        result = await orchestrator.conduct_mock_interview(
            interview_type=interview_type,
            question_number=question_number,
            previous_answer=previous_answer
        )
        return {"agent": "Kemi", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ STARTUP EVENT ============

@app.on_event("startup")
async def startup_event():
    """Log startup."""
    print("🚀 WDC Labs AI Backend starting...")
    print("✅ Gemini AI configured")
    print("✅ Agents: Tolu, Emem, Sola, Kemi ready")
    print("✅ Orchestrator initialized")
