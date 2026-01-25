"""
WDC Labs AI Backend
FastAPI application for the immersive virtual office AI system.
"""

import os
import io
import re
import json
import mimetypes
from typing import Optional
import PyPDF2
from dotenv import load_dotenv
import httpx
from docx import Document
import requests
import google.generativeai as genai
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from app.orchestrator import Orchestrator
from app.schemas import (
    ChatRequest, ChatResponse,
    BioAssessmentRequest, BioAssessmentResponse,
    SubmissionReviewRequest, SubmissionReviewResponse,
    PortfolioBulletRequest, PortfolioBulletResponse,
    OnboardingIntroRequest, OnboardingIntroResponse,
    OnboardingIntroMessage, AgentName,
    ResourceGenerationRequest, ResourceGenerationResponse
)
from app.task_templates import generate_task
from app.utils.file_extractor import extract_text_from_file


# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "WDC Labs AI Backend is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "gemini-2.5-flash",
        "agents": ["Tolu", "Emem", "Sola", "Kemi"]
    }

# ============ CHAT ============

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        return await orchestrator.route_message(
            message=request.message,
            context=request.context,
            chat_history=request.chat_history or []
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# ============ BIO ASSESSMENT ============

@app.post("/assess-bio", response_model=BioAssessmentResponse)
async def assess_bio(request: BioAssessmentRequest):
    try:
        bio_text = request.bio_text or ""
        cv_text = ""
        cv_url = request.cv_url or request.file_url

        if cv_url:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.get(cv_url, timeout=30.0)
                if res.status_code == 200:
                    if cv_url.lower().endswith(".pdf"):

                        reader = PyPDF2.PdfReader(io.BytesIO(res.content))
                        for page in reader.pages:
                            cv_text += page.extract_text() or ""
                    elif cv_url.lower().endswith(".docx"):
                        
                        doc = Document(io.BytesIO(res.content))
                        for p in doc.paragraphs:
                            cv_text += p.text + "\n"
                    else:
                        cv_text = res.text[:5000]

        if not bio_text and not cv_text:
            raise HTTPException(
                status_code=400,
                detail="Either bio_text, file_url, or cv_url must be provided"
            )

        assessment_text = bio_text
        if cv_text:
            assessment_text += f"\n\n[CV Content]\n{cv_text[:3000]}"

        result = await orchestrator.assess_bio(assessment_text, request.track)

        return BioAssessmentResponse(
            response_text=result.get("response_text"),
            assessed_level=result.get("assessed_level"),
            reasoning=result.get("reasoning"),
            warmup_mode=result.get("warmup_mode", False)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# ============ CV TRANSLATION ============

@app.post("/translate-to-cv", response_model=PortfolioBulletResponse)
async def translate_to_cv(request: PortfolioBulletRequest):
    try:
        from .agents import kemi
        result = await kemi.translate_to_cv_bullet(
            task_title=request.task_title,
            task_description=request.task_description,
            user_accomplishment=request.user_submission,
            model=model
        )
        return PortfolioBulletResponse(
            skill_tag=result.get("skill_tag"),
            bullet_point=result.get("bullet_point")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# ============ ONBOARDING INTRO ============

@app.post("/onboarding-intro", response_model=OnboardingIntroResponse)
async def generate_onboarding_intro(request: OnboardingIntroRequest):
    try:
        prompt = f"""
        Generate a scripted team introduction for a new intern named {request.user_name} joining the {request.track} track.
        
        The team consists of:
        - Tolu (Onboarding Officer): Professional, efficient. Example: "Welcome to WDC Labs."
        - Emem (Project Manager): Strict, deadline-driven. Example: "I need your first task by 5 PM."
        - Sola (Tech Lead): Critical, perfectionist. Example: "I'll be reviewing your code."
        - Kemi (Career Coach): Supportive, encouraging. Example: "I'm here to help you grow."

        Create a sequence of 4-6 short messages introducing themselves.
        
        Return ONLY valid JSON in this format:
        {{
            "messages": [
                {{ "agent": "Tolu", "message": "..." }},
                {{ "agent": "Emem", "message": "..." }},
                {{ "agent": "Sola", "message": "..." }},
                {{ "agent": "Kemi", "message": "..." }}
            ]
        }}
        """
        response = model.generate_content(prompt)
        match = re.search(r"\{.*\}", response.text, re.DOTALL)

        if not match:
            raise ValueError("Invalid AI response")

        data = json.loads(match.group())
        messages = []

        delay = 0
        for msg in data["messages"]:
            delay += max(1500, len(msg["message"]) * 60)
            messages.append(
                OnboardingIntroMessage(
                    agent=AgentName(msg["agent"]),
                    message=msg["message"],
                    typing_delay_ms=delay
                )
            )

        return OnboardingIntroResponse(messages=messages)

    except (ValueError, KeyError, TypeError):
        return OnboardingIntroResponse(messages=[])

# ============ WORK SUBMISSION REVIEW (FINAL + VALID) ============

@app.post("/review-submission", response_model=SubmissionReviewResponse)
async def review_submission(request: SubmissionReviewRequest):
    try:
        # Extract file content if URL is provided
        file_content = request.file_content or ""
        
        if request.file_url and request.file_url.startswith("http"):
            try:
                res = requests.get(request.file_url, timeout=30)
                if res.status_code == 200:
                    mime, _ = mimetypes.guess_type(request.file_url)
                    
                    # Use universal file extractor
                    extracted = extract_text_from_file(
                        file_url=request.file_url,
                        file_content_bytes=res.content,
                        mime_type=mime
                    )
                    
                    if extracted and extracted != "[Binary file - cannot extract text]":
                        file_content = extracted
                    else:
                        file_content += "\n[File uploaded - format not readable]"
                        
            except Exception as e:
                file_content += f"\n[Error reading file: {str(e)}]"
        
        # Call Sola's review function through orchestrator
        result = await orchestrator.review_submission(
            task_title=request.task_title,
            task_brief=request.task_brief,
            submission_content=file_content or request.file_content or "No content provided",
            client_constraints=None
        )
        
        return SubmissionReviewResponse(
            feedback=result.get("feedback", "Unable to generate review"),
            passed=result.get("passed", False),
            score=result.get("score", 0),
            portfolio_bullet=result.get("portfolio_bullet")
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Review submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Review failed: {str(e)}") from e

# ============ TASK GENERATION ============

class TaskRequest(BaseModel):
    track: str
    experience_level: str
    task_number: int
    user_city: Optional[str] = None
    user_name: str

@app.post("/generate-tasks")
def generate_tasks(req: TaskRequest):
    task = generate_task(
        track=req.track,
        difficulty=req.experience_level.lower(),
        task_number=req.task_number,
        user_city=req.user_city,
        user_name=req.user_name,
        model=model # Pass the AI model for content generation
    )
    return {"tasks": [task]}





# ============ RESOURCE GENERATION ============

# @app.post("/generate-resource", response_model=ResourceGenerationResponse)
# async def generate_resource(req: ResourceGenerationRequest):
#     try:
#         prompt = f"""
#         Generate a helpful educational resource based on this query:
        
#         Query: {req.query}
#         Track: {req.track}
#         User Level: {req.user_level or 'General'}
#         Task Context: {req.task_context or 'None'}
        
#         Create a resource with:
#         - Title: A clear, descriptive title
#         - Category: One word category (e.g., Tutorial, Guide, Reference, Example)
#         - Content: Markdown-formatted content with practical information
        
#         Keep content under 500 words. Make it educational and relevant.
#         Do NOT include any external links or URLs - focus on internal knowledge.
#         """
        
#         response = await model.generate_content_async(prompt)
#         content = response.text
        
#         # Clean any potential broken links (though we instructed not to include)
#         from app.utils.link_verifier import clean_broken_links
#         content = await clean_broken_links(content)
        
#         # Parse the response to extract title, category, content
#         lines = content.split('\n')
#         title = "Generated Resource"
#         category = "Guide"
#         content_body = content
        
#         for i, line in enumerate(lines):
#             if line.startswith('Title:'):
#                 title = line.replace('Title:', '').strip()
#             elif line.startswith('Category:'):
#                 category = line.replace('Category:', '').strip()
#             elif line.startswith('Content:'):
#                 content_body = '\n'.join(lines[i+1:]).strip()
#                 break
        
#         return ResourceGenerationResponse(
#             title=title,
#             category=category,
#             content=content_body
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# ============ STARTUP ============ 

@app.on_event("startup")
async def startup_event():
    print("🚀 WDC Labs AI Backend starting...")
    print("✅ Gemini configured")
    print("✅ Orchestrator ready")


# ============ HEALTH CHECK ============ 
@app.get("/health")
def health():
    return "ok"
