"""
WDC Labs Task Templates
Library of "Ungoogleable" task templates with messy data generation.
Includes ethical training scenarios and compliance checks.
"""

import random
import re
import json
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Internal app imports
from app.utils.deadline_formatter import format_deadline_display
from app.utils.link_verifier import clean_broken_links_sync
from app.curriculum import get_curriculum_step
from .agents import emem
from app.utils.db import get_cached_search, save_cached_search # <--- Added DB imports

# --- Industry contexts for task variation ---
INDUSTRIES = [
    "Fintech", "Agriculture", "Logistics", "Healthcare", "E-commerce",
    "Real Estate", "Education", "Energy", "Hospitality", "Manufacturing"
]

# --- Nigerian cities for localized context ---
NIGERIAN_CITIES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", 
    "Bayelsa", "Benue", "Borno", "Cross River", "Delta", 
    "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", 
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", 
    "Kwara", "Lagos", "Nassarawa", "Niger", "Ogun", "Ondo", 
    "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", 
    "Yobe", "Zamfara"
]

# --- Company name generators ---
COMPANY_PREFIXES = ["Tech", "Smart", "Prime", "Nova", "Apex", "Swift", "Core", "Global"]
COMPANY_SUFFIXES = ["Hub", "Labs", "Solutions", "Systems", "Ventures", "Group", "Corp"]

def generate_company_name(industry: str) -> str:
    """Generate a random but realistic company name."""
    _ = industry
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    city = random.choice(NIGERIAN_CITIES)
    return f"{city} {prefix} {suffix}"

# --- Inject realistic anomalies for data tasks ---
def inject_data_anomalies(data: List[Dict], anomaly_count: int = 3) -> tuple:
    """
    Inject realistic data anomalies into a dataset.
    Returns (corrupted_data, anomaly_descriptions)
    """
    anomaly_types = [
        "currency_conversion_error", "duplicate_row", 
        "null_value", "date_format_error", "decimal_shift"
    ]
    
    anomalies = []
    for _ in range(anomaly_count):
        row_idx = random.randint(0, len(data) - 1)
        anomaly_type = random.choice(anomaly_types)
        
        if anomaly_type == "currency_conversion_error":
            if "revenue" in data[row_idx]:
                original = data[row_idx]["revenue"]
                data[row_idx]["revenue"] = original * 1500  # NGN to USD error
                anomalies.append(f"Row {row_idx + 1}: Currency conversion error in revenue")
        
        elif anomaly_type == "duplicate_row":
            data.insert(row_idx + 1, data[row_idx].copy())
            anomalies.append(f"Row {row_idx + 1}: Duplicate entry")
        
        elif anomaly_type == "null_value":
            field = random.choice(list(data[row_idx].keys()))
            data[row_idx][field] = None
            anomalies.append(f"Row {row_idx + 1}: Missing value in {field}")
        
        elif anomaly_type == "date_format_error":
            if "date" in data[row_idx]:
                data[row_idx]["date"] = data[row_idx]["date"].replace("-", "/")
                anomalies.append(f"Row {row_idx + 1}: Inconsistent date format")
        
        elif anomaly_type == "decimal_shift":
            for key in data[row_idx]:
                if isinstance(data[row_idx][key], (int, float)) and key != "id":
                    data[row_idx][key] = data[row_idx][key] * 10
                    anomalies.append(f"Row {row_idx + 1}: Decimal shift in {key}")
                    break
    
    return data, anomalies

# --- Task templates by track ---
TASK_TEMPLATES = {
    "data_analytics": [
        {
            "title_template": "Data Cleansing: {company} Sales Data",
            "brief_template": """Clean {company}'s {month} {year} sales data CSV. {anomaly_count} anomalies caused by {error_cause}. Find them, fix data, calculate real ROAS.\n\n**Tasks:**\n- Identify anomalies\n- Document issues\n- Calculate corrected ROAS\n- 3-sentence summary""",
            "constraints": "Must use Python. No external libraries except pandas and numpy.",
            "difficulty_levels": ["beginner", "intermediate", "advanced"]
        },
        {
            "title_template": "{company} Customer Segmentation Analysis",
            "brief_template": """Analyze {company}'s customer dataset. Create segments based on purchase frequency, average order value, time since last purchase.\n\n**Deliverables:**\n1. 3+ customer segments\n2. Segment characteristics\n3. 1 marketing recommendation per segment""",
            "constraints": "Analysis must be reproducible. Document your methodology.",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ],
    "digital_marketing": [
        {
            "title_template": "SEO Audit: {company} Website",
            "brief_template": """Audit {company}'s website SEO. Client in {industry}, targeting {city} market.\n\n**Scope:**\n1. 5+ technical SEO issues\n2. On-page optimization opportunities\n3. Content gap analysis\n4. 3 competitor keywords""",
            "constraints": "Use only free tools. Screaming Frog free version is acceptable.",
            "difficulty_levels": ["beginner", "intermediate"]
        },
        {
            "title_template": "Social Media Campaign: {company} Product Launch",
            "brief_template": """Create 2-week social media campaign for {company}'s new product launch.\n\n**Requirements:**\n- Content calendar with post ideas\n- Platform strategies (Instagram, Twitter, LinkedIn)\n- Hashtag strategy\n- KPIs to track success\n\n**Budget:** ₦50,000 total.""",
            "constraints": "All content must be culturally appropriate for Nigerian audience.",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ],
    "cyber_security": [
        {
            "title_template": "Vulnerability Assessment: {company} Network",
            "brief_template": """Assess {company}'s network security. Review network diagram and configs.\n\n**Identify:**\n1. 3+ vulnerabilities\n2. Risk level (High/Medium/Low)\n3. Remediation steps\n4. Quick wins vs. long-term fixes""",
            "constraints": "Do not attempt active scanning. This is a passive assessment only.",
            "difficulty_levels": ["beginner", "intermediate", "advanced"]
        },
        {
            "title_template": "Security Policy Review: {company}",
            "brief_template": """Review {company}'s new security policy for gaps.\n\n**Focus Areas:**\n1. Password policy adequacy\n2. Incident response procedures\n3. Data classification gaps\n4. Access control weaknesses""",
            "constraints": "Recommendations must be practical for a small business (under 50 employees).",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ]
}

# --- Main task generation function ---
async def generate_task(
    user_name: str,
    track: str,
    deadline_display: str,
    experience_level: str = "",
    difficulty: str = "intermediate",
    task_number: int = 1,
    user_city: str = None,
    include_ethical_trap: bool = None,
    model=None,
    include_video_brief: bool = True,
    
) -> Dict[str, Any]:
    
    search_query = None  # Ensure always defined

    # Normalize track name
    track_key = track.lower().replace(" ", "_").replace("-", "_")
    if track_key not in TASK_TEMPLATES:
        track_key = "data_analytics"

    # Filter templates
    available_templates = [
        t for t in TASK_TEMPLATES[track_key]
        if difficulty.lower() in t.get("difficulty_levels", ["intermediate"])
    ]
    if not available_templates:
        available_templates = TASK_TEMPLATES[track_key]

    template = random.choice(available_templates)

    if include_ethical_trap is None:
        include_ethical_trap = random.random() < 0.25

    industry = random.choice(INDUSTRIES)
    city = user_city or random.choice(NIGERIAN_CITIES)
    company = generate_company_name(industry)

    now = datetime.now()
    month = now.strftime("%B")
    year = now.year

    error_causes = ["a currency conversion error", "a data import bug", "manual entry mistakes", "a timezone misconfiguration"]

    # Curriculum Check
    curriculum = get_curriculum_step(track_key, task_number)

    # -----------------------------
    # AI Curriculum Mode
    # -----------------------------
    if curriculum and model:
        prompt = f"""
        Generate a realistic workplace task brief for intern "{user_name}".
        Topic: {curriculum['topic']}
        Objective: {curriculum['objective']}
        Key Concepts: {', '.join(curriculum['key_concepts'])}
        Company: {company} in {city}

        CRITICAL REQUIREMENT for SOLA 2.0: The brief MUST explicitly ask the intern to submit a tangible file (.csv, .xlsx, .pdf, .docx, .py, or .sql) corresponding to their work so the Technical Lead can review it.

        Also provide:
        "educational_resources": one good Google search query string.

        Return JSON:
        {{
            "title": "...",
            "brief_template": "...",
            "constraints": "...",
            "educational_resources": "search query"
        }}
        """

        try:
            response = model.generate_content(prompt)
            match = re.search(r"\{.*\}", response.text, re.DOTALL)

            if match:
                gen_data = json.loads(match.group())
                title = gen_data.get("title") or "Generated Task"
                brief = gen_data.get("brief_template") or "Complete the assigned objective."
                search_query = gen_data.get("educational_resources") or f"{track} tutorial" 
                print("DEBUG SEARCH QUERY:", search_query)
                template["constraints"] = gen_data.get("constraints")
            else:
                raise ValueError("AI JSON parse failed")
        except Exception as e:
            print(f"Fallback to static due to: {e}")
            curriculum = None 

    # -----------------------------
    # Static Template Mode
    # -----------------------------
    if not (curriculum and model):
        title = template["title_template"].format(company=company, industry=industry, city=city)
        brief = template["brief_template"].format(
            company=company, industry=industry, city=city,
            month=month, year=year,
            anomaly_count=random.randint(2, 5),
            error_cause=random.choice(error_causes)
        )
        search_query = f"{track} tutorial for beginners"
        print("DEBUG SEARCH QUERY:", search_query)
        

    # -----------------------------
    # Ethical Trap
    # -----------------------------
    ethical_trap = None
    if include_ethical_trap:
        ethical_trap = generate_ethical_trap(track_key)
        brief += f"\n\n⚠️ Ethical Scenario:\n{ethical_trap['scenario']}\n"

    # -----------------------------
    # Deadline
    # -----------------------------
    deadline = now + timedelta(days=1)
    while deadline.weekday() >= 5:
        deadline += timedelta(days=1)

    deadline_display = format_deadline_display(deadline.isoformat())

    # -----------------------------
    # CACHED SERPER SEARCH
    # -----------------------------
    fetched_resources = []
    if search_query:
        # 1. Check if we already paid for this search
        cached_results = await get_cached_search(search_query)
        
        if cached_results:
            print("CACHE HIT! Serving resources from DB for:", search_query)
            fetched_resources = cached_results
        else:
            print("CACHE MISS! Calling Serper for:", search_query)
            serper_results = serper_search_links(search_query + " youtube tutorial OR practical guide")
            for res in serper_results:
                fetched_resources.append({
                    "link": res.get("url"),
                    "title": res.get("title"),
                    "description": res.get("snippet")
                })
            
            # 2. Save it for the next intern
            if fetched_resources:
                await save_cached_search(search_query, fetched_resources)


    # -----------------------------
    # Object Assembly
    # -----------------------------
    task_dict = {
        "title": title,
        "brief_content": brief.strip(),
        "difficulty": difficulty,
        "client_constraints": template.get("constraints"),
        "deadline": deadline.isoformat(),
        "experience_level": experience_level,
        "attachments": [], # <--- REDUNDANT PDF REMOVED
        "resources": fetched_resources, # <--- RICH DATA ADDED
        "ai_persona_config": {
            "role": "Supervisor",
            "tone": "professional",
            "expertise": track,
            "instruction": "Review submission thoroughly",
            "deadline_display": deadline_