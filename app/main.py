print("🚀 RUNNING THIS MAIN FILE:", __file__)

"""
WDC Labs AI Backend
Production-Grade FastAPI Backend
Immersive Virtual Office AI System
"""

# ============================================================
# STANDARD LIBRARIES
# ============================================================

import os
import io
import re
import json
import mimetypes
import asyncio
import logging

from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse

# ============================================================
# THIRD-PARTY LIBRARIES
# ============================================================

import httpx
import PyPDF2
import google.generativeai as genai

from dotenv import load_dotenv
from docx import Document

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# INTERNAL IMPORTS
# ============================================================

from app.orchestrator import Orchestrator

from app.schemas import (
    ChatRequest,
    ChatResponse,
    BioAssessmentRequest,
    BioAssessmentResponse,
    SubmissionReviewRequest,
    SubmissionReviewResponse,
    PortfolioBulletRequest,
    PortfolioBulletResponse,
    OnboardingIntroRequest,
    OnboardingIntroResponse,
    OnboardingIntroMessage,
    AgentName,
    MockInterviewRequest,
    MockInterviewResponse
)

from app.task_templates import generate_task

from app.utils.file_extractor import extract_text_from_file

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ============================================================
# ENVIRONMENT LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / ".env.production"

load_dotenv(dotenv_path=env_path)

logger.info(
    f"GEMINI LOADED: "
    f"{bool(os.getenv('GEMINI_API_KEY'))}"
)

# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is required"
    )

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================================
# APPLICATION SERVICES
# ============================================================

orchestrator = Orchestrator(model)

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="WDC Labs AI Backend",
    description=(
        "Immersive Virtual Office AI System "
        "with Multi-Agent Architecture"
    ),
    version="2.0.0"
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

ALLOWED_ORIGINS = [
    "https://labs.wdc.ng",
    "https://www.labs.wdc.ng",
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# SAFE FILE URL HOSTS - SSRF PROTECTION
# ============================================================

ALLOWED_FILE_HOSTS = [
    "supabase.co",
    "amazonaws.com",
    "s3.amazonaws.com",
    "storage.googleapis.com"
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def is_safe_external_url(url: str) -> bool:
    """
    Production-safe SSRF protection.
    """
    try:
        parsed = urlparse(url)
        hostname = (
            parsed.hostname or ""
        ).lower()

        return any(
            hostname == allowed
            or hostname.endswith(f".{allowed}")
            for allowed in ALLOWED_FILE_HOSTS
        )
    except Exception:
        return False


def prune_task_title(task_title: str) -> str:
    """
    Smart query pruning wrapper.
    Removes filler/stop words and captures the top 4 
    highly meaningful subject keywords for precision searching.
    """
    stop_words = {
        "a", "an", "the", "for", "to", "with", "and", "of", "in", "on",
        "using", "build", "create", "develop", "design", "challenge"
    }

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        task_title.lower()
    )

    meaningful_words = [
        word
        for word in words
        if word not in stop_words
    ]

    return " ".join(
        meaningful_words[:4]
    )


def safe_json_response(response) -> Dict[str, Any]:
    """
    Safe synchronous JSON parsing helper.
    """
    try:
        return response.json()
    except Exception as e:
        logger.error(
            f"JSON PARSE ERROR: {str(e)}"
        )
        return {}


def deduplicate_links(
    links: List[str],
    max_links: int = 15
) -> List[str]:
    """
    Ordered deduplication with cap.
    """
    seen = set()
    deduped = []

    for link in links:
        normalized = link.strip()
        if (
            normalized
            and normalized not in seen
        ):
            seen.add(normalized)
            deduped.append(normalized)

    return deduped[:max_links]

# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "WDC Labs AI Backend is running"
    }

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "gemini-2.5-flash",
        "agents": [
            "Tolu",
            "Emem",
            "Sola",
            "Kemi"
        ]
    }

# ============================================================
# CHAT ENDPOINT
# ============================================================

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
        logger.exception("CHAT ERROR")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e

# ============================================================
# BIO ASSESSMENT
# ============================================================

@app.post(
    "/assess-bio",
    response_model=BioAssessmentResponse
)
async def assess_bio(request: BioAssessmentRequest):
    try:
        bio_text = request.bio_text or ""
        cv_text = ""
        cv_url = request.cv_url or request.file_url

        if cv_url:
            if not is_safe_external_url(cv_url):
                raise HTTPException(
                    status_code=400,
                    detail="Unsafe file URL detected"
                )

            async with httpx.AsyncClient(
                timeout=30.0
            ) as client:
                res = await client.get(cv_url)
                if res.status_code == 200:
                    if cv_url.lower().endswith(".pdf"):
                        reader = PyPDF2.PdfReader(
                            io.BytesIO(res.content)
                        )
                        for page in reader.pages:
                            cv_text += (
                                page.extract_text() or ""
                            )
                    elif cv_url.lower().endswith(".docx"):
                        doc = Document(
                            io.BytesIO(res.content)
                        )
                        for p in doc.paragraphs:
                            cv_text += p.text + "\n"
                    else:
                        cv_text = res.text[:5000]

        if not bio_text and not cv_text:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Either bio_text, file_url, "
                    "or cv_url must be provided"
                )
            )

        assessment_text = bio_text
        if cv_text:
            assessment_text += (
                f"\n\n[CV Content]\n{cv_text[:3000]}"
            )

        result = await orchestrator.assess_bio(
            assessment_text,
            request.track
        )

        return BioAssessmentResponse(
            response_text=result.get("response_text"),
            assessed_level=result.get("assessed_level"),
            reasoning=result.get("reasoning"),
            warmup_mode=result.get(
                "warmup_mode",
                False
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("BIO ASSESSMENT ERROR")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e

# ============================================================
# CV TRANSLATION
# ============================================================

@app.post(
    "/translate-to-cv",
    response_model=PortfolioBulletResponse
)
async def translate_to_cv(
    request: PortfolioBulletRequest
):
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
        logger.exception("CV TRANSLATION ERROR")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e

# ============================================================
# MOCK INTERVIEW
# ============================================================

@app.post(
    "/mock-interview",
    response_model=MockInterviewResponse
)
async def mock_interview(
    request: MockInterviewRequest
):
    try:
        from .agents import kemi

        result = await kemi.conduct_mock_interview(
            interview_type=request.interview_type,
            question_number=request.question_number,
            previous_answer=request.previous_answer,
            model=model,
            interview_subtype=request.interview_subtype
        )

        return MockInterviewResponse(
            stage=result.get("stage"),
            question_number=result.get("question_number"),
            content=result.get("content"),
            question=result.get("content"),
            tip=result.get("tip"),
            evaluation=result.get("evaluation")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("MOCK INTERVIEW ERROR")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) from e

# ============================================================
# ONBOARDING INTRO
# ============================================================

@app.post(
    "/onboarding-intro",
    response_model=OnboardingIntroResponse
)
async def generate_onboarding_intro(
    request: OnboardingIntroRequest
):
    try:
        prompt = f"""
        Generate a scripted onboarding introduction
        for a new intern named {request.user_name}
        joining the {request.track} track.

        Return ONLY valid JSON.
        """

        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        if not getattr(response, "text", None):
            raise ValueError(
                "Gemini returned empty response"
            )

        try:
            data = json.loads(response.text)
        except Exception:
            match = re.search(
                r"\{.*\}",
                response.text,
                re.DOTALL
            )
            if not match:
                raise ValueError(
                    "Invalid AI JSON response"
                )
            data = json.loads(match.group())

        messages = []
        delay = 0

        for msg in data["messages"]:
            delay += max(
                1500,
                len(msg["message"]) * 60
            )

            messages.append(
                OnboardingIntroMessage(
                    agent=AgentName(msg["agent"]),
                    message=msg["message"],
                    typing_delay_ms=delay
                )
            )

        return OnboardingIntroResponse(
            messages=messages
        )
    except Exception as e:
        logger.exception("ONBOARDING ERROR")
        return OnboardingIntroResponse(
            messages=[]
        )

# ============================================================
# SUBMISSION REVIEW
# ============================================================

@app.post(
    "/review-submission",
    response_model=SubmissionReviewResponse
)
async def review_submission(
    request: SubmissionReviewRequest
):
    try:
        file_content = request.file_content or ""

        if (
            request.file_url
            and request.file_url.startswith("http")
        ):
            if not is_safe_external_url(
                request.file_url
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Unsafe file URL detected"
                )

            try:
                async with httpx.AsyncClient(
                    timeout=30.0
                ) as client:
                    res = await client.get(
                        request.file_url
                    )

                if res.status_code == 200:
                    mime, _ = mimetypes.guess_type(
                        request.file_url
                    )
                    extracted = extract_text_from_file(
                        file_url=request.file_url,
                        file_content_bytes=res.content,
                        mime_type=mime
                    )

                    if (
                        extracted
                        and extracted != (
                            "[Binary file - cannot extract text]"
                        )
                    ):
                        file_content = extracted
                    else:
                        file_content += (
                            "\n[Unreadable uploaded file]"
                        )
            except Exception as e:
                logger.error(
                    f"FILE EXTRACTION ERROR: {str(e)}"
                )

        result = await orchestrator.review_submission(
            task_title=request.task_title,
            task_brief=request.task_brief,
            submission_content=(
                file_content
                or request.file_content
                or "No content provided"
            ),
            client_constraints=None,
            attempt_number=request.attempt_number
        )

        return SubmissionReviewResponse(
            feedback=result.get(
                "feedback",
                "Unable to generate review"
            ),
            passed=result.get("passed", False),
            score=result.get("score", 0),
            portfolio_bullet=result.get(
                "portfolio_bullet"
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("SUBMISSION REVIEW ERROR")
        raise HTTPException(
            status_code=500,
            detail=f"Review failed: {str(e)}"
        ) from e

# ============================================================
# TASK REQUEST MODEL
# ============================================================

class TaskRequest(BaseModel):
    user_name: str
    track: str
    deadline_display: str
    experience_level: Optional[str] = ""
    difficulty: Optional[str] = "intermediate"
    task_number: Optional[int] = 1
    user_city: Optional[str] = None
    include_ethical_trap: Optional[bool] = False
    include_video_brief: Optional[bool] = True

# ============================================================
# SERPER RESOURCE ENRICHMENT
# ============================================================

async def fetch_serper_resources(
    track: str,
    task_title: str,
    api_key: str
) -> Dict[str, Any]:

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    discovered_links: List[str] = []
    cache_results: List[Dict[str, Any]] = []

    pruned_title = prune_task_title(task_title)
    logger.info(f"SEARCH QUERY TITLE: {pruned_title}")

    async with httpx.AsyncClient(
        timeout=10.0
    ) as client:

        # ====================================================
        # DOCUMENTATION / PDF SWEEP
        # ====================================================
        try:
            web_query = (
                f"{track} "
                f"{pruned_title} "
                f"tutorial guide filetype:pdf"
            )
            web_res = await client.post(
                "https://google.serper.dev/search",
                headers=headers,
                json={
                    "q": web_query,
                    "num": 4
                }
            )

            if web_res.status_code == 200:
                data = safe_json_response(web_res)
                organic = data.get("organic", [])

                if not organic:
                    fallback_query = (
                        f"{track} "
                        f"{pruned_title} "
                        f"tutorial guide documentation"
                    )
                    web_res = await client.post(
                        "https://google.serper.dev/search",
                        headers=headers,
                        json={
                            "q": fallback_query,
                            "num": 4
                        }
                    )
                    data = safe_json_response(web_res)
                    organic = data.get("organic", [])

                for item in organic:
                    if not isinstance(item, dict):
                        continue

                    link = item.get("link")
                    if not link:
                        continue

                    discovered_links.append(link)
                    is_pdf = (
                        link.lower().endswith(".pdf")
                        or "pdf" in item.get("title", "").lower()
                    )

                    cache_results.append({
                        "title": item.get(
                            "title",
                            f"Documentation: {task_title}"
                        ),
                        "link": link,
                        "url": link,
                        "snippet": item.get(
                            "snippet",
                            "Official reference material."
                        ),
                        "type": "pdf" if is_pdf else "web",
                        "category": "Reference Links"
                    })

        except Exception as e:
            logger.error(f"DOCUMENT SEARCH ERROR: {str(e)}")

        # ====================================================
        # VIDEO SWEEP
        # ====================================================
        try:
            video_query = (
                f"{track} "
                f"{pruned_title} "
                f"tutorial video"
            )
            video_res = await client.post(
                "https://google.serper.dev/videos",
                headers=headers,
                json={
                    "q": video_query,
                    "num": 3
                }
            )

            if video_res.status_code == 200:
                data = safe_json_response(video_res)
                videos = data.get("videos", [])

                for item in videos:
                    if not isinstance(item, dict):
                        continue

                    link = item.get("link")
                    if not link:
                        continue

                    discovered_links.append(link)

                    cache_results.append({
                        "title": item.get(
                            "title",
                            (
                                f"Video Tutorial: "
                                f"{task_title}"
                            )
                        ),
                        "link": link,
                        "url": link,
                        "snippet": item.get(
                            "snippet",
                            "Hands-on video guidance."
                        ),
                        "type": "video",
                        "category": "Video Resources"
                    })

        except Exception as e:
            logger.error(f"VIDEO SEARCH ERROR: {str(e)}")

    return {
        "links": discovered_links,
        "cache_results": cache_results
    }

# ============================================================
# SUPABASE CACHE SYNC
# ============================================================

async def sync_search_cache(
    query: str,
    results: List[Dict[str, Any]]
):
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or os.getenv("SUPABASE_ANON_KEY")
    )

    if (
        not SUPABASE_URL
        or not SUPABASE_SERVICE_KEY
        or not results
    ):
        return

    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    payload = {
        "query": query.lower().strip(),
        "results": results
    }

    try:
        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/search_cache",
                headers=headers,
                json=payload
            )

            if response.status_code >= 400:
                logger.error(
                    f"SUPABASE CACHE ERROR: "
                    f"{response.status_code} | "
                    f"{response.text}"
                )
            else:
                logger.info("SUPABASE CACHE SYNC SUCCESS")

    except Exception as e:
        logger.error(
            f"SUPABASE CACHE FAILURE: {str(e)}"
        )

# ============================================================
# TASK GENERATION ENDPOINT (WITH DEEP SCRUBBING ENGINE)
# ============================================================

@app.post("/generate-tasks")
async def generate_tasks(req: TaskRequest):
    try:
        task = await generate_task(
            user_name=req.user_name,
            track=req.track,
            deadline_display=req.deadline_display,
            experience_level=req.experience_level,
            difficulty=req.difficulty,
            task_number=req.task_number,
            user_city=req.user_city,
            include_ethical_trap=req.include_ethical_trap,
            model=model,
            include_video_brief=req.include_video_brief
        )

        if not isinstance(task, dict):
            raise HTTPException(
                status_code=500,
                detail=(
                    "Task generation returned "
                    "invalid response format"
                )
            )

        # =================================================
        # PLATFORM-WIDE TITLE SANITIZATION SWEEP
        # =================================================
        if "title" in task and isinstance(task["title"], str):
            raw_title = task["title"]
            user_name = req.user_name

            # Level 1: Wipe exact case-insensitive username strings + common dividers
            if user_name.lower() in raw_title.lower():
                raw_title = re.sub(
                    rf"{re.escape(user_name)}\s*[:\-\|]*\s*", 
                    "", 
                    raw_title, 
                    flags=re.IGNORECASE
                )
            
            # Level 2: Strict colon partition purge to clear lingering role prefixes
            if ":" in raw_title:
                raw_title = raw_title.split(":")[-1]

            # Lock the sanitized pure subject back into the platform task payload
            task["title"] = raw_title.strip()

        # =================================================
        # RESOURCE ENRICHMENT ON CLEAN SUBJECT
        # =================================================
        SERPER_API_KEY = os.getenv(
            "SERPER_API_KEY"
        )

        if SERPER_API_KEY:
            task_title = task.get(
                "title",
                "tutorial"
            )

            enrichment = await fetch_serper_resources(
                track=req.track,
                task_title=task_title,
                api_key=SERPER_API_KEY
            )

            discovered_links = enrichment.get(
                "links",
                []
            )

            cache_results = enrichment.get(
                "cache_results",
                []
            )

            if discovered_links:
                existing_resources = task.get(
                    "educational_resources",
                    ""
                )

                all_links = []

                if (
                    existing_resources
                    and isinstance(
                        existing_resources,
                        str
                    )
                ):
                    all_links.extend([
                        link.strip()
                        for link in (
                            existing_resources.split(",")
                        )
                        if link.strip()
                    ])

                all_links.extend(discovered_links)
                
                deduped_links = deduplicate_links(
                    all_links,
                    max_links=15
                )

                task["educational_resources"] = ",".join(deduped_links)

            if cache_results:
                cache_query = f"{req.track} {task_title}"
                await sync_search_cache(
                    query=cache_query,
                    results=cache_results
                )

        return {
            "tasks": [task]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("TASK GENERATION ERROR")
        raise HTTPException(
            status_code=500,
            detail=(
                f"Task generation failed: "
                f"{str(e)}"
            )
        ) from e

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 WDC Labs AI Backend starting...")
    logger.info("✅ Gemini configured")
    logger.info("✅ Orchestrator ready")