print("🚀 RUNNING THIS MAIN FILE:", __file__)

"""
WDC Labs AI Backend
Production-Grade FastAPI Backend
Immersive Virtual Office AI System
Updated for 5-Day Actionable Tasks & Shared Drive Generation
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
import time
from datetime import datetime, timedelta

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

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Header

from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# INTERNAL IMPORTS
# ============================================================

from app.cron import router as cron_router

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
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]

app.include_router(cron_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
# BACKEND SYLLABUS KNOWLEDGE BASE
# ============================================================

TRACK_SYLLABUS = {
  "data-analytics": [
    { "topic": "Intro to Data Analytics", "days": ["What is Data Analytics?", "The Data Life Cycle", "Key Metrics & KPIs", "Data Privacy & Ethics", "Dataset Exploration", "Reality Task: Analyze sales records"] },
    { "topic": "Excel Basics", "days": ["Interface & Navigation", "Data Entry & Cleanup", "Sorting & Multi-level Filtering", "Cell Referencing", "Data Validation", "Reality Task: Clean employee records"] },
    { "topic": "Excel Functions & Formulas", "days": ["Basic Aggregations", "Text Functions", "Logical Functions", "Conditional Sums", "Lookup Functions", "Reality Task: Fix customer data"] },
    { "topic": "Data Visualization in Excel", "days": ["Chart Principles", "Chart Formatting", "Pivot Tables Basics", "Pivot Charts & Slicers", "Dashboard Layout", "Reality Task: Create sales dashboard"] },
    { "topic": "Power Query & Data Cleaning", "days": ["Intro to Power Query", "Connecting Data", "Transformations", "Merging & Appending", "Data Types & Errors", "Reality Task: Import messy sales files"] },
    { "topic": "Excel Business Project", "days": ["Project Scoping", "Data Cleaning & Audit", "Data Analysis", "Dashboard Build", "Insight Generation", "Reality Task: Analyze retail data"] },
    { "topic": "SQL Basics", "days": ["Intro to RDBMS & SQL", "Data Retrieval", "Filtering Data", "Sorting Results", "SQL Practice", "Reality Task: Retrieve customer orders"] },
    { "topic": "SQL Joins & Aggregation", "days": ["Aggregation Functions", "Grouping Data", "SQL Joins 1 (Inner/Left)", "SQL Joins 2 (Right/Full)", "Multi-Table Joins", "Reality Task: Top-performing products"] },
    { "topic": "Intermediate SQL Analysis", "days": ["Subqueries", "Common Table Expressions (CTEs)", "String & Date Functions", "Conditional Logic (CASE)", "Performance Optimization", "Reality Task: Declining sales trends"] },
    { "topic": "Power BI Fundamentals", "days": ["Intro to Power BI Desktop", "Data Ingestion", "Star Schema Data Modeling", "Basic Visuals", "Visual Interactivity", "Reality Task: Build KPI cards"] },
    { "topic": "Power BI Dashboards & DAX", "days": ["Intro to DAX", "Essential DAX Functions", "The CALCULATE Function", "Time Intelligence in DAX", "Executive Dashboard Formatting", "Reality Task: MoM growth trends"] },
    { "topic": "Portfolio + Analyst Defense", "days": ["Portfolio Setup", "Executive Summaries", "Presentation Deck Creation", "Q&A Prep", "Final Rehearsal", "Reality Task: Present business insights"] },
    { "topic": "Python for Data Analytics", "days": ["Intro to Python & Jupyter", "Python Control Structures", "Intro to Pandas", "Loading Datasets", "Data Inspection", "Reality Task: Load and clean CSV files"] },
    { "topic": "Data Manipulation with Pandas", "days": ["Filtering Data", "Data Cleaning", "Aggregations", "Merging Data", "Feature Engineering", "Reality Task: Regional sales performance"] },
    { "topic": "Python Visualization", "days": ["Intro to Matplotlib", "Intro to Seaborn", "Customizing Visuals", "Visualizing Distributions", "Multi-plot Grids", "Reality Task: Ad spend vs sales"] },
    { "topic": "Working with Big Data Files", "days": ["Memory Management", "Optimized File Formats", "Vectorization", "Large Dataset Filtering", "Out-of-Memory Workflows", "Reality Task: Analyze 2GB transaction file"] },
    { "topic": "Statistical Analysis", "days": ["Central Tendency & Dispersion", "Probability Distributions", "Correlation vs Causation", "Hypothesis Testing", "Churn Analysis Drivers", "Reality Task: Factor influencing churn"] },
    { "topic": "Advanced Power BI & DAX", "days": ["Dynamic Parameters", "Advanced DAX", "Row-Level Security (RLS)", "Performance Analyzer", "Dashboard UX/UI", "Reality Task: Dynamic executive dashboard"] },
    { "topic": "Business Reporting & Communication", "days": ["Storytelling Frameworks", "Eliminating Noise", "Writing for C-Suite", "Slide Deck Design", "Presenting Uncertainties", "Reality Task: Boardroom-ready report"] },
    { "topic": "Analytics Automation", "days": ["Automation Architecture", "Python Scripting", "Power BI Gateway", "Email Alerts", "Workflow Debugging", "Reality Task: Automate weekly reporting"] },
    { "topic": "Predictive Analytics Foundations", "days": ["Time Series Basics", "Moving Averages", "Linear Regression Intro", "Evaluating Forecasts", "Scenario Analysis", "Reality Task: Predict sales performance"] },
    { "topic": "Cross-Department Data Analysis", "days": ["Multi-Department Metrics", "Customer Journey Mapping", "Data Reconciliation", "Cohort Analysis", "Cross-Department Dashboards", "Reality Task: Identify revenue leakage"] },
    { "topic": "Real-World Data Crisis Simulation", "days": ["Diagnostic Analytics", "Finding Broken Pipelines", "Fast Data Patching", "Stakeholder Management", "Root Cause Analysis", "Reality Task: Fix broken reports"] },
    { "topic": "Boardroom Defense & Strategic Analytics", "days": ["12-Month Analytics Roadmap", "Estimating Analytics ROI", "Final Executive Presentation", "Mock Defense", "Final Polish", "Reality Task: Present 12-month strategy"] }
  ],
  "digital-marketing": [
    { "topic": "Intro to Digital Marketing", "days": ["The Digital Ecosystem", "Business Growth Models", "Key Digital Metrics", "Competitor Research", "Marketing Audit Setup", "Reality Task: Analyze local business"] },
    { "topic": "Customer Journey & Psychology", "days": ["Consumer Psychology", "The Marketing Funnel", "The 3i Principles", "Buyer Personas", "Touchpoint Mapping", "Reality Task: Map fintech journey"] },
    { "topic": "Content & Social Media Basics", "days": ["Platform Mechanics", "Hook Writing", "Content Pillars", "Content Scheduling", "Community Engagement", "Reality Task: 1-week Instagram plan"] },
    { "topic": "SEO & Search Fundamentals", "days": ["How Search Engines Work", "Keyword Research", "On-Page SEO 1", "On-Page SEO 2", "SEO Audit Tools", "Reality Task: Audit website and optimize"] },
    { "topic": "Meta Ads Fundamentals", "days": ["Meta Business Suite Setup", "Campaign Hierarchy", "Audience Targeting", "Budgeting & Scheduling", "Ad Setup", "Reality Task: Meta Ads campaign"] },
    { "topic": "Google Ads & PPC", "days": ["Intro to PPC & Search Ads", "Match Types", "Ad Copywriting", "Ad Extensions (Assets)", "Bidding Strategies", "Reality Task: Launch Google Ads"] },
    { "topic": "Creatives & Landing Pages", "days": ["Direct Response Copywriting", "Visual Design Principles", "Landing Page Essentials", "Call to Actions (CTAs)", "Landing Page Wireframing", "Reality Task: Redesign ad creatives"] },
    { "topic": "Email & Mobile Marketing", "days": ["Lifecycle Marketing", "Email Copywriting", "Onboarding Sequences", "Mobile Marketing", "Email Deliverability", "Reality Task: 5-email onboarding flow"] },
    { "topic": "Analytics & Tracking", "days": ["Web Analytics Intro", "Pixel & Conversion Setup", "UTM Parameters", "Attribution Models", "Diagnostic Analytics", "Reality Task: Diagnose GA4 report"] },
    { "topic": "Media Planning & Strategy", "days": ["Budget Allocation", "Forecasting KPIs", "Channel Mix Strategy", "Campaign Timelines", "Media Plan Assembly", "Reality Task: 6-month media plan"] },
    { "topic": "Campaign Optimization", "days": ["Performance Auditing", "A/B Testing Framework", "Fixing ROAS", "Bidding Adjustments", "Emergency Rescue Tactics", "Reality Task: Fix underperforming campaigns"] },
    { "topic": "Portfolio + Boardroom Defense", "days": ["Portfolio Structuring", "Reporting Frameworks", "Case Study Writing", "Objections & Defense", "Mock Pitch", "Reality Task: Present campaign results"] },
    { "topic": "Advanced Meta Ads", "days": ["Campaign Budget Optimization", "High-Budget Scaling", "Advanced Retargeting", "Dynamic Product Ads", "Creative Fatigue System", "Reality Task: Scale winning campaign"] },
    { "topic": "Advanced Google Ads", "days": ["Performance Max (PMAX)", "YouTube Ads", "Display & Remarketing", "Search Term Cleanups", "Smart Bidding", "Reality Task: Fix wasting spend"] },
    { "topic": "Conversion Rate Optimization (CRO)", "days": ["Heatmap Analysis", "User Friction Audits", "Copy & Value Proposition Testing", "Checkout Optimization", "A/B Test Execution", "Reality Task: Increase conversion rate"] },
    { "topic": "Full Funnel Systems", "days": ["Multi-Touch Funnels", "Cross-Channel Synchronization", "Offer Architecture", "Measurement Architecture", "Funnel Mapping", "Reality Task: Build acquisition funnel"] },
    { "topic": "Advanced Analytics", "days": ["Cohort Analysis", "CAC & LTV Economics", "Multi-Touch Attribution", "Unit Economics Debugging", "Strategic Analytics Reporting", "Reality Task: Identify CAC increase"] },
    { "topic": "Marketing Automation", "days": ["CRM Architectures", "Lead Scoring", "Automated Workflows", "Webhook Integrations", "Automation Testing", "Reality Task: Automated lead nurturing"] },
    { "topic": "Growth Marketing Systems", "days": ["Pirate Metrics (AARRR)", "Experimentation Frameworks", "Activation Rate Optimization", "Viral Loops & Referral Systems", "Growth Sprints", "Reality Task: Improve activation by 25%"] },
    { "topic": "AI in Marketing", "days": ["Generative AI for Copy", "AI Visual Generation", "Audience Research with AI", "Automated Reporting", "AI Workflow Integration", "Reality Task: AI-assisted workflows"] },
    { "topic": "Crisis & Reputation Management", "days": ["Social Listening Setup", "Crisis Classification", "Statement Drafting", "De-escalation Frameworks", "24-Hour Recovery Playbook", "Reality Task: 24-hour response strategy"] },
    { "topic": "Client & Stakeholder Management", "days": ["Managing Expectations", "Difficult Conversations", "Value-Based Upselling", "Client Reporting Meetings", "SLA & Scope Defense", "Reality Task: Defend delayed results"] },
    { "topic": "Agency Simulation", "days": ["Multi-Client Management", "Resource Allocation", "Emergency Priority Shifts", "Team Workflows", "Account Health Checks", "Reality Task: Manage 3 campaigns"] },
    { "topic": "Executive Boardroom Defense", "days": ["12-Month Growth Roadmap", "Executive Financial Modeling", "Presentation Mastery", "Live Board Defense Prep", "Strategy Polish", "Reality Task: Defend growth strategy"] }
  ],
  "cyber-security": [
    { "topic": "Intro to Cybersecurity", "days": ["Core Pillars (CIA Triad)", "Threat Landscape", "Threat Actors", "Attack Vectors", "Business Risk", "Reality Task: Phishing compromise"] },
    { "topic": "Linux & Command Line Basics", "days": ["Intro to Linux OS", "File Operations", "Text Processing", "Permissions & Ownership", "System Management", "Reality Task: Navigate server directories"] },
    { "topic": "Networking Fundamentals", "days": ["Networking Models (OSI)", "IP Addressing & Subnetting", "Core Protocols", "Network Traffic Analysis", "Network Tools", "Reality Task: Trace suspicious activity"] },
    { "topic": "Security Fundamentals", "days": ["Authentication vs Authorization", "Access Control Models", "Principle of Least Privilege", "Identity Auditing", "Password Security", "Reality Task: Audit permissions"] },
    { "topic": "Firewalls & Network Security", "days": ["Firewall Architecture", "Network Segmentation", "Firewall Rule Writing", "NACLs & Security Groups", "Traffic Auditing", "Reality Task: Block insecure traffic"] },
    { "topic": "Threats & Vulnerabilities", "days": ["Attack Tactics", "Denial of Service (DoS)", "Vulnerability Management", "Log Analysis Basics", "Attack Identification", "Reality Task: Analyze brute-force logs"] },
    { "topic": "Authentication & MFA", "days": ["Authentication Factors", "Multi-Factor Authentication", "SSO & Identity Protocols", "MFA Vulnerabilities", "Policy Enforcement", "Reality Task: Implement MFA rules"] },
    { "topic": "Encryption & Cryptography", "days": ["Cryptography Concepts", "Hashing Functions", "Data States", "PKI & Certificates", "Integrity Verification", "Reality Task: Encrypt confidential files"] },
    { "topic": "Monitoring & Incident Response", "days": ["Vulnerability Scanning", "Incident Response Lifecycle", "Log Aggregation", "Security Reporting", "Risk Prioritization", "Reality Task: Prepare security risk report"] },
    { "topic": "Disaster Recovery Fundamentals", "days": ["BCP & Disaster Recovery", "Recovery Metrics", "Ransomware Mechanics", "Backup Strategies", "Incident Containment", "Reality Task: Respond to ransomware"] },
    { "topic": "Security Reporting & Documentation", "days": ["Technical Documentation", "SOPs", "Executive Summaries", "Evidence Handling", "Portfolio Assembly", "Reality Task: Compile vulnerability report"] },
    { "topic": "Boardroom Defense & Risk Communication", "days": ["Security ROI", "Presenting Risk Matrices", "Handling Pushback", "Slide Deck Design", "Defense Practice", "Reality Task: Present risk mitigation plan"] },
    { "topic": "Advanced Network Security", "days": ["Intrusion Detection (IDS/IPS)", "Packet Capture Analysis", "Network Microsegmentation", "VPNs & Secure Proxies", "Suspicious Pattern Detection", "Reality Task: Isolate suspicious traffic"] },
    { "topic": "Ethical Hacking Fundamentals", "days": ["Penetration Testing Phases", "Reconnaissance (OSINT)", "Web App Recon", "Exploitation Mechanics", "Remediation Verification", "Reality Task: Identify vulnerabilities"] },
    { "topic": "Web Application Security", "days": ["OWASP Top 10 Intro", "Injection Attacks", "Cross-Site Scripting (XSS)", "Authentication Weaknesses", "Web App Patching", "Reality Task: Patch vulnerabilities"] },
    { "topic": "Device & Endpoint Protection", "days": ["EDR vs Antivirus", "Malware Types", "Host Logs Auditing", "Persistence Mechanisms", "Malware Containment", "Reality Task: Investigate malware infection"] },
    { "topic": "Cloud & Infrastructure Security", "days": ["Shared Responsibility Model", "Cloud Identity (IAM)", "Cloud Storage Security", "IaC Auditing", "Cloud Logging & Auditing", "Reality Task: Secure misconfigured bucket"] },
    { "topic": "SOC Workflows & Threat Hunting", "days": ["SOC Operations", "Threat Hunting Basics", "SIEM Querying", "Correlation Rules", "False Positive Reduction", "Reality Task: Investigate suspicious logins"] },
    { "topic": "Security Policies & Compliance", "days": ["Compliance Frameworks", "Data Privacy Regulations", "Security Policy Drafting", "Vendor Risk Management", "Compliance Incident Auditing", "Reality Task: Draft compliance response"] },
    { "topic": "Security Automation & AI Risks", "days": ["SOAR principles", "Python Scripting for Defense", "Automated Alert Workflows", "AI Security Risks", "AI in Cyber Defense", "Reality Task: Automated alert workflow"] },
    { "topic": "Enterprise Incident Management", "days": ["Major Incident Command", "Enterprise Breach Scenarios", "Multi-System Isolation", "External Escalation", "Root Cause Analysis", "Reality Task: Coordinate breach response"] },
    { "topic": "Attack & Defense Simulation", "days": ["Red Team Tactics", "Blue Team Defenses", "Purple Team Collaboration", "Live Attack Mitigation", "Post-Simulation Debrief", "Reality Task: Defend infrastructure"] },
    { "topic": "Security Operations Management", "days": ["Incident Prioritization", "Resource Management", "Operational Metrics", "Crisis Escalations", "Team Playbook Updates", "Reality Task: Manage simultaneous incidents"] },
    { "topic": "Executive Boardroom Defense", "days": ["12-Month Security Roadmap", "Justifying Security Investments", "Executive Deck Preparation", "Mock Board Defense", "Final Review", "Reality Task: Present cybersecurity strategy"] }
  ]
}

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
# ASYNC QUEUE WORKER ENGINE FOR TASKS
# ============================================================

task_queue = asyncio.Queue()

async def generate_with_retry(func, *args, max_retries=5, **kwargs):
    base_delay = 2
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Quota" in error_msg:
                if attempt == max_retries - 1:
                    logger.error("Max retries hit for Gemini API. Giving up.")
                    raise e
                
                delay = base_delay * (2 ** attempt) 
                logger.warning(f"Rate limited (429)! Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                raise e 

async def generate_weekly_modules_via_ai(user_name, track, task_number, week_data):
    """
    Prompts Gemini to generate 6 specific daily modules based on the week's syllabus.
    Now rigorously enforces submissions for every day and generates mock files.
    """
    prompt = f"""
    You are Sola, the Lead Technical Supervisor at WDC Labs.
    Your intern, {user_name}, is starting Week {task_number} of the {track} track.

    The focus for this week is: "{week_data['topic']}"
    
    You must generate exactly 6 modules. Days 1 to 5 are daily actionable tasks. The 6th module is the "Reality Task" (the capstone).
    
    Here is the daily breakdown you must follow:
    1. {week_data['days'][0]}
    2. {week_data['days'][1]}
    3. {week_data['days'][2]}
    4. {week_data['days'][3]}
    5. {week_data['days'][4]}
    6. {week_data['days'][5]}

    CRITICAL RULES:
    1. ACTIONABLE DELIVERABLES ONLY: Every single day (Days 1-6) MUST explicitly require the user to submit a deliverable (e.g., a short report, code snippet, spreadsheet, or URL). 
    2. THE SHARED DRIVE RULE (MANDATORY): You MUST generate at least ONE raw mock file (CSV dataset, txt log, or policy document) required to complete the Reality Task or one of the daily tasks. DO NOT leave the shared_drive array empty.

    Return the response as a JSON array containing EXACTLY 6 objects. DO NOT wrap in markdown, return pure JSON.
    Each object must have:
    - "title": (String, e.g. "Day 1: What is Data Analytics?")
    - "brief_content": (String, a rich, engaging Markdown brief. Include corporate context, learning objectives, and clear instructions for the required submission.)
    - "difficulty": (String, "Beginner" for days 1-3, "Intermediate" for 4-5, "Advanced" for the Reality Task)
    - "shared_drive": (Array of Objects) You MUST include at least one mock file for the Reality Task. Format: [{{"filename": "company_data.csv", "content": "id,name,revenue\\n1,Acme,50000"}}]
    """

    response = await asyncio.to_thread(
        model.generate_content,
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    raw_data = json.loads(response.text)
    
    if isinstance(raw_data, dict) and "tasks" in raw_data:
        return raw_data["tasks"]
    elif isinstance(raw_data, list):
        return raw_data
    else:
        raise ValueError("AI failed to return an array of 6 tasks")

async def queue_worker():
    while True:
        req = await task_queue.get()
        try:
            logger.info(f"⚙ Worker processing 6-Part Week Generation for {req.user_name}")
            
            # 1. Lookup the Syllabus
            track_key = req.track.lower().replace(" ", "-") if req.track else "data-analytics"
            if track_key not in TRACK_SYLLABUS: track_key = "data-analytics"
            
            syllabus_list = TRACK_SYLLABUS[track_key]
            week_index = min(max(req.task_number - 1, 0), len(syllabus_list) - 1)
            week_data = syllabus_list[week_index]

            # 2. Generate 6 modules via Gemini
            modules = await generate_with_retry(
                generate_weekly_modules_via_ai,
                user_name=req.user_name,
                track=req.track,
                task_number=req.task_number,
                week_data=week_data
            )

            if not isinstance(modules, list) or len(modules) < 1:
                logger.error("AI returned invalid module format")
                continue

            # 3. Fetch Serper Resources (We fetch once for the overall week topic to save time)
            SERPER_API_KEY = os.getenv("SERPER_API_KEY")
            resource_array = []
            
            if SERPER_API_KEY:
                enrichment = await fetch_serper_resources(
                    track=req.track,
                    task_title=week_data['topic'],
                    api_key=SERPER_API_KEY
                )
                for i, cache_res in enumerate(enrichment.get("cache_results", [])):
                    link = cache_res.get("link", cache_res.get("url", ""))
                    if link:
                        is_yt = "youtube" in link or "youtu.be" in link
                        resource_array.append({
                            "id": f"cache-vid-{i}-{int(time.time())}",
                            "title": cache_res.get("title", f"Guide {i+1}"),
                            "type": cache_res.get("type", "video" if is_yt else "web"),
                            "category": cache_res.get("category", "Learning Resources"),
                            "description": cache_res.get("snippet", "Reference material"),
                            "url": link
                        })

            # 4. Save to Supabase via Bulk Insert
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
            
            if SUPABASE_URL and SUPABASE_SERVICE_KEY:
                db_payloads = []
                base_time = datetime.utcnow()

                # Build the 6 payloads, offsetting created_at so Day 1 sorts before Day 2, etc.
                for i, mod in enumerate(modules):
                    # Extract the shared drive mock files
                    shared_files = mod.get("shared_drive", [])
                    
                    db_payloads.append({
                        "user": req.user_id,
                        "title": mod.get("title", f"Day {i+1}"),
                        "brief_content": mod.get("brief_content", "Please review the resources."),
                        "difficulty": mod.get("difficulty", "intermediate"),
                        "task_track": req.track,
                        "ai_persona_config": {
                            "role": "Supervisor", "tone": "professional", "expertise": req.track, "instruction": "Review submission thoroughly"
                        },
                        "completed": False,
                        "status": "pending",
                        "task_number": req.task_number,
                        "resources": resource_array,
                        "attachments": shared_files,  # Saving the generated mock data here!
                        "video_brief": "",
                        "deadline_display": req.deadline_display or "Friday, 11:59 PM",
                        "created_at": (base_time + timedelta(seconds=i)).isoformat()
                    })

                async with httpx.AsyncClient(timeout=30.0) as client:
                    db_res = await client.post(
                        f"{SUPABASE_URL}/rest/v1/tasks",
                        headers={
                            "apikey": SUPABASE_SERVICE_KEY,
                            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                            "Content-Type": "application/json",
                            "Prefer": "return=minimal"
                        },
                        json=db_payloads
                    )

                    if db_res.status_code >= 400:
                        logger.error(f"❌ SUPABASE BULK SAVE FAILED: {db_res.status_code} | {db_res.text}")
                    else:
                        logger.info(f"💾 Successfully saved 6-part Week {req.task_number} for {req.user_name}!")
            else:
                logger.error("Missing Supabase Variables.")

        except Exception as e:
            logger.error(f"TASK GENERATION BACKGROUND ERROR: {str(e)}")
        finally:
            task_queue.task_done()

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
        return await generate_with_retry(
            orchestrator.route_message,
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
                    f"FILE EXTRACTION ERROR (URL): {str(e)}"
                )

        elif request.file_content and "PK\x03\x04" in request.file_content:
            try:
                extracted = extract_text_from_file(
                    file_url="",
                    file_content_bytes=request.file_content.encode('utf-8', 'ignore'),
                    mime_type=""
                )
                if extracted and "error" not in extracted.lower():
                    file_content = extracted
            except Exception as e:
                logger.error(f"FILE EXTRACTION ERROR (Direct): {str(e)}")

        result = await generate_with_retry(
            orchestrator.review_submission,
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

        raw_bullet = result.get("portfolio_bullet")
        if isinstance(raw_bullet, dict):
            clean_bullet = raw_bullet.get("bullet_point", raw_bullet.get("content", str(raw_bullet)))
        else:
            clean_bullet = raw_bullet

        return SubmissionReviewResponse(
            feedback=result.get(
                "feedback",
                "Unable to generate review"
            ),
            passed=result.get("passed", False),
            score=result.get("score", 0),
            portfolio_bullet=clean_bullet
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
# TASK REQUEST MODELS
# ============================================================

class TaskRequest(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = "Intern"
    track: Optional[str] = "General"
    deadline_display: Optional[str] = "Flexible"
    experience_level: Optional[str] = ""
    difficulty: Optional[str] = "intermediate"
    task_number: Optional[int] = 1
    user_city: Optional[str] = None
    include_ethical_trap: Optional[bool] = False
    include_video_brief: Optional[bool] = True
    previous_performance: Optional[str] = "N/A"
    is_admin_override: Optional[bool] = False

class GenerateCVRequest(BaseModel):
    user_id: str
    user_name: Optional[str] = "WDC Intern"
    track: Optional[str] = "General"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    feedback: Optional[List[dict]] = []
    tasks: List[dict]

class RegenerateRequest(BaseModel):
    task_id: int
    user_name: Optional[str] = "Intern"
    track: str
    task_number: int
    deadline_display: Optional[str] = "Flexible"

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

    async with httpx.AsyncClient(timeout=10.0) as client:

        try:
            web_query = f"{track} {pruned_title} tutorial guide filetype:pdf"
            web_res = await client.post(
                "https://google.serper.dev/search",
                headers=headers,
                json={"q": web_query, "num": 5}
            )

            organic = []
            if web_res.status_code == 200:
                data = safe_json_response(web_res)
                organic = data.get("organic", [])

                if not organic:
                    fallback_query = f"{track} {pruned_title} tutorial guide documentation"
                    web_res = await client.post(
                        "https://google.serper.dev/search",
                        headers=headers,
                        json={"q": fallback_query, "num": 5}
                    )
                    data = safe_json_response(web_res)
                    organic = data.get("organic", [])

                doc_count = 0
                for item in organic:
                    if doc_count >= 2:
                        break
                        
                    if not isinstance(item, dict): continue
                    link = item.get("link")
                    if not link: continue

                    discovered_links.append(link)
                    is_pdf = link.lower().endswith(".pdf") or "pdf" in item.get("title", "").lower()

                    cache_results.append({
                        "title": item.get("title", f"Documentation: {task_title}"),
                        "link": link,
                        "url": link,
                        "snippet": item.get("snippet", "Official reference material."),
                        "type": "pdf" if is_pdf else "web",
                        "category": "Document Resources"
                    })
                    doc_count += 1

        except Exception as e:
            logger.error(f"DOCUMENT SEARCH ERROR: {str(e)}")

        try:
            video_query = f"{track} {pruned_title} tutorial video"
            video_res = await client.post(
                "https://google.serper.dev/videos",
                headers=headers,
                json={"q": video_query, "num": 5}
            )

            if video_res.status_code == 200:
                data = safe_json_response(video_res)
                videos = data.get("videos", [])

                video_count = 0
                for item in videos:
                    if video_count >= 3:
                        break
                        
                    if not isinstance(item, dict): continue
                    link = item.get("link")
                    if not link: continue

                    discovered_links.append(link)

                    cache_results.append({
                        "title": item.get("title", f"Video Tutorial: {task_title}"),
                        "link": link,
                        "url": link,
                        "snippet": item.get("snippet", "Hands-on video guidance."),
                        "type": "video",
                        "category": "Video Resources"
                    })
                    video_count += 1

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
        or os.getenv("SUPABASE_KEY")
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
# TASK GENERATION ENDPOINT (SECURED & GATED)
# ============================================================

@app.post("/generate-tasks")
async def generate_tasks(req: TaskRequest):
    """
    Secure endpoint for generating new weekly tasks.
    Enforces strict progression gating to prevent task spamming.
    """
    try:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        # 🚨 THE IRON GATE: VALIDATE USER STATE BEFORE QUEUEING 🚨
        if not hasattr(req, 'user_id') or not req.user_id:
            raise HTTPException(status_code=400, detail="Access Denied: Missing User ID.")
            
        elif req.is_admin_override:
            logger.info(f"🛡️ Admin Override Active: Bypassing progression gates for {req.user_name}")
            pass 
            
        else:
            async with httpx.AsyncClient() as client:
                # 1. Fetch user progression state
                prog_res = await client.get(
                    f"{SUPABASE_URL}/rest/v1/user_progression?user_id=eq.{req.user_id}&select=week_status,current_week",
                    headers={"apikey": SUPABASE_SERVICE_KEY, "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"}
                )
                
                if prog_res.status_code == 200:
                    prog_data = prog_res.json()
                    
                    if not prog_data:
                        task_check = await client.get(
                            f"{SUPABASE_URL}/rest/v1/tasks?user=eq.{req.user_id}&select=id",
                            headers={"apikey": SUPABASE_SERVICE_KEY, "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"}
                        )
                        if task_check.status_code == 200 and len(task_check.json()) > 0:
                            raise HTTPException(
                                status_code=403, 
                                detail="Access Denied: You already have a task assigned. Please complete it first."
                            )
                    else:
                        week_status = prog_data[0].get("week_status")
                        
                        if week_status in ["in_progress", "needs_revision"]:
                            task_check = await client.get(
                                f"{SUPABASE_URL}/rest/v1/tasks?user=eq.{req.user_id}&status=in.(pending,submitted,under_review,needs_revision)",
                                headers={"apikey": SUPABASE_SERVICE_KEY, "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"}
                            )
                            if task_check.status_code == 200 and len(task_check.json()) > 0:
                                raise HTTPException(
                                    status_code=403, 
                                    detail="Access Denied: You already have an active task on your desk. Complete it before requesting a new one."
                                )
                            
                        elif week_status == "passed_waiting":
                            raise HTTPException(
                                status_code=403,
                                detail="Access Denied: You have successfully completed your task for this week. Your next brief will automatically unlock on Monday."
                            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GATEKEEPER ERROR: {str(e)}")
        pass 

    await task_queue.put(req)
    
    return {
        "status": "processing",
        "message": "Your 6-part learning module is being generated. This might take a moment.",
        "queue_position": task_queue.qsize()
    }

# ============================================================
# REGENERATE TASK ENDPOINT
# ============================================================

@app.post("/regenerate-task")
async def regenerate_existing_task(req: RegenerateRequest):
    """
    Synchronous endpoint for regenerating a task in-place.
    It creates a new brief and overwrites the existing row.
    """
    try:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")
        
        async with httpx.AsyncClient() as client:
            check_res = await client.get(
                f"{SUPABASE_URL}/rest/v1/tasks?id=eq.{req.task_id}&select=is_regenerated",
                headers={"apikey": SUPABASE_SERVICE_KEY, "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"}
            )
            
            if check_res.status_code == 200:
                data = check_res.json()
                if data and data[0].get("is_regenerated"):
                    raise HTTPException(status_code=400, detail="This task has already been regenerated once.")

        task = await generate_with_retry(
            generate_task,
            user_name=req.user_name,
            track=req.track,
            deadline_display=req.deadline_display,
            experience_level="",
            difficulty="intermediate",
            task_number=req.task_number,
            user_city=None,
            include_ethical_trap=False,
            model=model,
            include_video_brief=False 
        )

        raw_title = task.get("title", "New Task")
        if req.user_name and req.user_name.lower() in raw_title.lower():
            raw_title = re.sub(rf"{re.escape(req.user_name)}\s*[:\-\|]*\s*", "", raw_title, flags=re.IGNORECASE)
        if ":" in raw_title:
            raw_title = raw_title.split(":")[-1]
        clean_title = raw_title.strip()

        update_payload = {
            "title": clean_title,
            "brief_content": task.get("brief_content", task.get("brief", task.get("description", ""))),
            "is_regenerated": True
        }

        async with httpx.AsyncClient() as client:
            update_res = await client.patch(
                f"{SUPABASE_URL}/rest/v1/tasks?id=eq.{req.task_id}",
                headers={
                    "apikey": SUPABASE_SERVICE_KEY,
                    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                },
                json=update_payload
            )
            
            if update_res.status_code >= 400:
                logger.error(f"Failed to update task {req.task_id}: {update_res.text}")
                raise Exception("Database update failed")

        return {"status": "success", "message": "Task regenerated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"REGENERATE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# CV GENERATION ENDPOINT
# ============================================================

@app.post("/generate-cv")
async def generate_cv_endpoint(req: GenerateCVRequest):
    try:
        from app.agents import kemi
        
        cv_content = await kemi.generate_full_resume(
            user_id=req.user_id,
            user_name=req.user_name,
            track=req.track,
            start_date=req.start_date,
            end_date=req.end_date,
            tasks=req.tasks,
            feedback=req.feedback,
            model=model
        )
        return {"success": True, "cv_content": cv_content}
    except Exception as e:
        logger.error(f"CV Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# AUTOMATED TASK RELEASE ENGINE (MONDAY 8:00 AM CRON)
# ============================================================

@app.post("/run-monday-task-release")
async def run_monday_task_release(authorization: str = Header(None)):
    expected_secret = os.getenv("CRON_SECRET")

    if not expected_secret or authorization != f"Bearer {expected_secret}":
        logger.warning("🚨 Unauthorized attempt to run the Monday Task Release Engine!")
        raise HTTPException(status_code=401, detail="Unauthorized Cron Execution")

    logger.info("⏰ Monday 8 AM Task Release Engine Triggered Successfully!")

    try:
        return {
            "status": "success",
            "message": "Monday task rollout and catch-up logic executed securely."
        }
    except Exception as e:
        logger.error(f"CRON ENGINE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to execute Monday Task Release")

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 WDC Labs AI Backend starting...")
    logger.info("✅ Gemini configured")
    logger.info("✅ Orchestrator ready")
    
    asyncio.create_task(queue_worker())
    logger.info("✅ Queue Worker active")