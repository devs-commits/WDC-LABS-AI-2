"""
WDC Labs Task Templates
Library of "Ungoogleable" task templates with messy data generation.
Includes ethical training scenarios and compliance checks.
"""

import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.utils.deadline_formatter import format_deadline_display
from app.utils.link_verifier import clean_broken_links_sync
from .agents import emem

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
        "currency_conversion_error",
        "duplicate_row",
        "null_value",
        "date_format_error",
        "decimal_shift"
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
    # DATA ANALYTICS
    "data_analytics": [
        {
            "title_template": "Data Cleansing: {company} Sales Data",
            "brief_template": """
Clean {company}'s {month} {year} sales data CSV. {anomaly_count} anomalies caused by {error_cause}. Find them, fix data, calculate real ROAS.

**Tasks:**
- Identify anomalies
- Document issues  
- Calculate corrected ROAS
- 3-sentence summary
""",
            "constraints": "Must use Python. No external libraries except pandas and numpy.",
            "difficulty_levels": ["beginner", "intermediate", "advanced"]
        },
        {
            "title_template": "{company} Customer Segmentation Analysis",
            "brief_template": """
Analyze {company}'s customer dataset. Create segments based on purchase frequency, average order value, time since last purchase.

**Deliverables:**
1. 3+ customer segments
2. Segment characteristics  
3. 1 marketing recommendation per segment
""",
            "constraints": "Analysis must be reproducible. Document your methodology.",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ],
    
    # DIGITAL MARKETING
    "digital_marketing": [
        {
            "title_template": "SEO Audit: {company} Website",
            "brief_template": """
Audit {company}'s website SEO. Client in {industry}, targeting {city} market.

**Scope:**
1. 5+ technical SEO issues
2. On-page optimization opportunities
3. Content gap analysis
4. 3 competitor keywords

**Note:** Website has intentional errors. Find them.
""",
            "constraints": "Use only free tools. Screaming Frog free version is acceptable.",
            "difficulty_levels": ["beginner", "intermediate"]
        },
        {
            "title_template": "Social Media Campaign: {company} Product Launch",
            "brief_template": """
Create 2-week social media campaign for {company}'s new product launch.

**Requirements:**
- Content calendar with post ideas
- Platform strategies (Instagram, Twitter, LinkedIn)
- Hashtag strategy
- KPIs to track success

**Budget:** ₦50,000 total.
""",
            "constraints": "All content must be culturally appropriate for Nigerian audience.",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ],
    
    # CYBER-SECURITY
    "cyber_security": [
        {
            "title_template": "Vulnerability Assessment: {company} Network",
            "brief_template": """
Assess {company}'s network security. Review network diagram and configs.

**Identify:**
1. 3+ vulnerabilities
2. Risk level (High/Medium/Low)
3. Remediation steps
4. Quick wins vs. long-term fixes

**Note:** Configs have common misconfigurations. Document them.
""",
            "constraints": "Do not attempt active scanning. This is a passive assessment only.",
            "difficulty_levels": ["beginner", "intermediate", "advanced"]
        },
        {
            "title_template": "Security Policy Review: {company}",
            "brief_template": """
Review {company}'s new security policy for gaps.

**Focus Areas:**
1. Password policy adequacy
2. Incident response procedures
3. Data classification gaps
4. Access control weaknesses

Provide recommendations with priority rankings.
""",
            "constraints": "Recommendations must be practical for a small business (under 50 employees).",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ]
}

# --- Resource Content Library ---
RESOURCE_CONTENT = {
    "da_guide_01": """
# Pandas Cheat Sheet for Data Cleaning

## 1. Handling Missing Data
```python
# Check for null values
df.isnull().sum()

# Drop rows with nulls
df.dropna()

# Fill nulls with mean/median
df['column'].fillna(df['column'].mean(), inplace=True)
```

## 2. Removing Duplicates
```python
# Check duplicates
df.duplicated().sum()

# Drop duplicates
df.drop_duplicates(inplace=True)
```

## 3. Data Type Conversion
```python
# Convert to datetime
df['date'] = pd.to_datetime(df['date'])

# Convert to numeric
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
```
""",
    "da_guide_02": """
# ROAS Calculation Template

**Formula:**
$$ ROAS = \\frac{\\text{Revenue from Ad}}{\\text{Cost of Ad}} $$

## Steps to Calculate
1. **Clean Revenue Data**: Ensure currency symbols are removed and values are numeric.
2. **Clean Cost Data**: Handle any missing or zero cost entries (avoid division by zero).
3. **Calculate per Campaign**:
   ```python
   df['ROAS'] = df['revenue'] / df['cost']
   ```
4. **Benchmark**:
   - ROAS < 4: Poor
   - ROAS > 4: Good
   - ROAS > 8: Excellent
""",
    "dm_guide_01": """
# SEO Basics: Technical Audit Checklist

## 1. Crawlability
- [ ] Check robots.txt (is it blocking important pages?)
- [ ] Verify XML Sitemap existence
- [ ] Check for 404 errors (Broken links)

## 2. On-Page Elements
- [ ] Title Tags: Are they unique and under 60 chars?
- [ ] Meta Descriptions: Do they exist and encourage clicks?
- [ ] H1 Tags: One per page, containing primary keyword.

## 3. Performance
- [ ] Page Load Speed (< 3s is ideal)
- [ ] Mobile Responsiveness check
- [ ] Image Optimization (Alt tags + sizing)
""",
    "dm_guide_02": """
# Social Media Campaign Template

## Campaign Overview
- **Goal**: [Brand Awareness / Conversion / Engagement]
- **Target Audience**: [Demographics / Interests]
- **Duration**: [Start Date] - [End Date]

## Platform Strategy
### Instagram (Visuals)
- Feed Posts: 3x per week (High quality product shots)
- Stories: Daily (Behind the scenes, Polls)
- Reels: 2x per week (Trends, Educational)

### LinkedIn (Professional)
- Thought Leadership: 1x per week
- Company Updates: 1x per week

## KPI Tracking
| Metric | Goal |
|--------|------|
| Impressions | 10,000 |
| Clicks | 500 |
| Engagement Rate | 3.5% |
""",
    "cyber_guide_01": """
# Vulnerability Assessment Checklist

## Network Security
1. **Firewall Configuration**: Are default ports closed?
2. **Access Control**: Is Least Privilege enforced?
3. **Wi-Fi**: Is WPA3 encryption enabled?

## System Hardening
1. **Patch Management**: Are all systems updated?
2. **Default Accounts**: Have default passwords been changed?
3. **Services**: Are unnecessary services disabled?

## Monitoring
1. Is logging enabled?
2. Are alerts configured for suspicious activity?
""",
    "cyber_guide_02": """
# Security Policy Template Structure

1. **Purpose**: Why does this policy exist?
2. **Scope**: Who and what does it apply to?
3. **Policy Statement**: The core rules.
   - *Password Requirements*: (Length, complexity, rotation)
   - *Access Control*: (RBAC, MFA)
   - *Data Handling*: (Classification, encryption)
4. **Enforcement**: Penalties for non-compliance.
5. **Review Cycle**: How often is this updated?
""",
    "general_01": """
# Reference Hint Document

## How to Approach This Task
1. **Read the Brief Carefully**: Identify the key deliverables.
2. **Check Constraints**: Are there format or tool restrictions?
3. **Plan Your Steps**: Break the problem down.
4. **Validate**: Double-check your work against the requirements.

## Troubleshooting
- **Missing Data?** Document it as a finding.
- **Ambiguous Instructions?** Make a reasonable assumption and state it clearly.
- **Stuck?** Check the specific guides for your track.
"""
}

RESOURCE_METADATA = [
    {"id": "da_guide_01", "title": "Pandas Cheat Sheet", "type": "code", "tags": ["csv", "data", "cleaning"], "track": "data_analytics"},
    {"id": "da_guide_02", "title": "ROAS Calculation Template", "type": "sheet", "tags": ["roas", "financial", "metrics"], "track": "data_analytics"},
    {"id": "dm_guide_01", "title": "SEO Basics PDF", "type": "pdf", "tags": ["seo", "audit", "website"], "track": "digital_marketing"},
    {"id": "dm_guide_02", "title": "Social Media Campaign Template", "type": "doc", "tags": ["campaign", "social", "calendar"], "track": "digital_marketing"},
    {"id": "cyber_guide_01", "title": "Vulnerability Checklist", "type": "sheet", "tags": ["vulnerability", "network", "assessment"], "track": "cybersecurity"},
    {"id": "cyber_guide_02", "title": "Security Policy Template", "type": "doc", "tags": ["policy", "review", "access"], "track": "cybersecurity"},
    {"id": "general_01", "title": "General Task Workflow", "type": "doc", "tags": [], "track": "general"}
]

# Build the Archive Library map for easy lookup
ARCHIVE_LIBRARY = {
    "data_analytics": [],
    "digital_marketing": [],
    "cybersecurity": [],
    "general": []
}

for meta in RESOURCE_METADATA:
    # Add content relative to ID
    item = {
        "id": meta["id"],
        "title": meta["title"],
        "tags": meta["tags"],
        "content": RESOURCE_CONTENT.get(meta["id"], "Content not found.")
    }
    
    if meta["track"] in ARCHIVE_LIBRARY:
        ARCHIVE_LIBRARY[meta["track"]].append(item)

def select_task_resources(task_brief: str, track: str) -> list:
    """
    Select 2-3 relevant internal resources for this task.
    """
    resources = []
    task_lower = task_brief.lower()
    
    for resource_item in ARCHIVE_LIBRARY.get(track, []):
        if any(tag in task_lower for tag in resource_item["tags"]):
            resources.append(resource_item)
    
    # Always add a general reference hint
    resources += ARCHIVE_LIBRARY.get("general", [])[:1]
    
    return resources[:3]  # max 3 resources
# --- Main task generation function ---
async def generate_task(
    # user_id: int,
    user_name: str,
    track: str,
    difficulty: str = "intermediate",
    task_number: int = 1,
    user_city: str = None,
    include_ethical_trap: bool = None,
    model = None,
    include_video_brief: bool = True
) -> Dict[str, Any]:
    """
    Generate a unique, ungoogleable task based on track and difficulty.
    20-30% of tasks include ethical traps to test professional judgment.
    """
    print("track was: ", track)
    # Normalize track name
    track_key = track.lower().replace(" ", "_")
    track_key = track_key.lower().replace("-", "_")
    if track_key not in TASK_TEMPLATES:
        track_key = "data_analytics"
    
    # Filter templates by difficulty
    available_templates = [
        t for t in TASK_TEMPLATES[track_key]
        if difficulty.lower() in t.get("difficulty_levels", ["intermediate"])
    ]
    if not available_templates:
        available_templates = TASK_TEMPLATES[track_key]
    
    template = random.choice(available_templates)
    
    # Determine if this task includes ethical trap (20-30% of tasks)
    if include_ethical_trap is None:
        include_ethical_trap = random.random() < 0.25  # 25% chance
    
    # Generate random context
    industry = random.choice(INDUSTRIES)
    city = user_city or random.choice(NIGERIAN_CITIES)
    company = generate_company_name(industry)
    
    # Date context
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year
    
    # Error causes for data tasks
    error_causes = [
        "a currency conversion error",
        "a data import bug",
        "manual entry mistakes",
        "a timezone misconfiguration"
    ]
    
    # Format the template
    # CHECK FOR CURRICULUM OVERRIDE
    from app.curriculum import get_curriculum_step
    curriculum = get_curriculum_step(track_key, task_number)

    if curriculum and model:
        # Generate fully dynamic task based on curriculum
        company = generate_company_name(industry)
        
        prompt = f"""
        Generate a concise task brief for an intern named "{user_name}" at a {industry} company named {company}.
        
        **Curriculum Logic:**
        - Task Number: {task_number}
        - Topic: {curriculum['topic']}
        - Learning Objective: {curriculum['objective']}
        - Key Concepts to Test: {', '.join(curriculum['key_concepts'])}
        
        **Context:**
        - City: {city}
        - Current Date: {month} {year}
        
        **Instructions:**
        Create a realistic workplace scenario (Task Title and Brief).
        Address the intern directly by name ("Dear {user_name}").
        The intern should feel like they are solving a real problem for the business.
        Include specific data points or file references (e.g., "attached sales_data.csv").
        Keep the brief concise, under 150 words.
        
        **Output Format (JSON):**
        {{
            "title": "Professional Task Title",
            "brief_template": "Concise brief...",
            "constraints": "Specific constraints..."
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            # Simple cleanup to find JSON
            import json
            import re
            match = re.search(r"\{.*\}", response.text, re.DOTALL)
            if match:
                gen_data = json.loads(match.group())
                title = gen_data.get("title")
                brief = gen_data.get("brief_template")
                template["constraints"] = gen_data.get("constraints") # Override constrains
            else:
                raise ValueError("Failed to parse AI curriculum task")
                 
        except (ValueError, RuntimeError, json.JSONDecodeError) as e:
            print(f"Curriculum generation failed: {e}. Falling back to curriculum-static mode.")
            # Fallback to Curriculum Static Mode (prevents random tasks)
            title = f"{curriculum['topic']}: {company}"
            brief = f"""
**Topic:** {curriculum['topic']}
**Objective:** {curriculum['objective']}

Dear {user_name},
At {company} in {city}, complete the objective above.

**Key Concepts:** {', '.join(curriculum['key_concepts'])}

Use provided tools.
"""
            template["constraints"] = "Standard professional constraints apply."

    else:
        # STANDARD TEMPLATE LOGIC
        title = template["title_template"].format(company=company, industry=industry, city=city)
        brief = template["brief_template"].format(
            company=company,
            industry=industry,
            city=city,
            month=month,
            year=year,
            anomaly_count=random.randint(2, 5),
            error_cause=random.choice(error_causes)
        )
    
    # ADD ETHICAL TRAP IF APPLICABLE
    ethical_trap = None
    if include_ethical_trap:
        ethical_trap = generate_ethical_trap(track_key)
        brief += f"\n\n**⚠️ ETHICAL CONSIDERATION:**\n{ethical_trap['scenario']}\n"
    
    # deadline - 1 day, excluding weekends
    deadline = now + timedelta(days=1)
    while deadline.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
        deadline += timedelta(days=1)
    duration_days = (deadline - now).days
    deadline_display = format_deadline_display(deadline.isoformat())


    # --- Resource selection ---
    # Pick relevant metadata first
    resource_metadata = select_task_resources(brief, track_key)
    
    educational_resources = []
    
    # If model is available, use AI to generate the content dynamically
    if model:
        for resource_meta in resource_metadata:
            try:
                # Generate dynamic content based on title, brief, and industry context
                prompt = f"""
                Create a practical, short "Cheat Sheet" or "Guide" for an intern working on this task:
                
                Task: {title}
                Industry: {industry}
                Topic: {resource_meta['title']}
                Tags: {resource_meta['tags']}
                
                Include code snippets (if technical), checklists, or step-by-step instructions.
                Keep it under 200 words. Make it look like a real internal document.
                """
                
                response = model.generate_content(prompt)
                content = response.text
                
                # Clean any broken links from the generated content
                content = clean_broken_links_sync(content)
                
                educational_resources.append({
                    "title": resource_meta["title"],
                    "description": f"AI-Generated Resource for {company}",
                    "content": content
                })
            except (ValueError, RuntimeError, ConnectionError) as e:
                print(f"Error generating resource content: {e}")
                # Fallback to static content
                educational_resources.append({
                    "title": resource_meta["title"],
                    "description": f"Internal Resource ({resource_meta['id']})",
                    "content": RESOURCE_CONTENT.get(meta["id"], "Content not available.")
                })
    else:
        # Fallback if no model provided
        educational_resources = [
            {"title": r["title"], "description": f"Internal Resource ({r['id']})", "content": r["content"]}
            for r in select_task_resources(brief, track_key)
        ]
    
    # --- Build final task dict ---
    task_dict = {
        "title": title,
        "brief_content": brief.strip(),
        "difficulty": difficulty,
        "client_constraints": template.get("constraints"),
        "deadline": deadline.isoformat(),
        "deadline_display": deadline_display,
        "attachments": [],
        "ai_persona_config": {
            "role": "Supervisor",
            "tone": "professional",
            "expertise": track,
            "instruction": "Review submission thoroughly",
            "duration": f"{duration_days} day"
        },
        "metadata": {
            "company": company,
            "industry": industry,
            "city": city,
            "task_number": task_number,
            "has_ethical_trap": include_ethical_trap,
            "ethical_trap": ethical_trap
        },
        "educational_resources": educational_resources,
        "video_brief": None # placeholder for now
    }

    # ---- VIDEO BRIEF (Emem) ----
    if model and include_video_brief:
        video_script = await emem.generate_video_brief_script(
            title,
            brief,
            model
        )

        # Calculate duration based on script length (approx 150 words/minute)
        word_count = len(video_script.split())
        duration_seconds = max(30, int((word_count / 150) * 60))  # Min 30 seconds

        task_dict["video_brief"] = {
            "agent": "Emem",
            "persona": "Sharp Nigerian Female Executive",
            "accent": "en-NG",
            "duration_seconds": duration_seconds,
            "script": video_script,
            "video_url": None,
            "status": "simulated"
        }

    return task_dict


# ============================================
# ETHICAL TRAP GENERATION
# ============================================

def generate_ethical_trap(track: str) -> Dict[str, str]:
    """
    Generate an ethical decision point tailored to the track.
    Returns {scenario, expected_response, why_it_matters}
    """
    
    ethical_traps_by_track = {
        "data_analytics": [
            {
                "scenario": "Client wants you to exclude certain demographic groups from the analysis 'because they skew the numbers.' The data clearly shows their inclusion is necessary for accuracy.",
                "expected_response": "Refuse. Present complete, unbiased analysis. Explain that selective reporting violates professional ethics and could be illegal.",
                "why_it_matters": "Discrimination law, professional ethics, data integrity"
            },
            {
                "scenario": "Your analysis shows the client's product is underperforming. They ask you to 'adjust the metrics' to show positive results before presenting to investors.",
                "expected_response": "Refuse. Present honest findings. Suggest alternative interpretations if they exist, but never falsify data.",
                "why_it_matters": "Fraud prevention, professional integrity, investor protection"
            },
            {
                "scenario": "Client sends you login credentials via email to access their database. Standard practice would be to use an API or secure authentication method.",
                "expected_response": "Refuse credentials. Ask for secure alternative (API, VPN, proper access management).",
                "why_it_matters": "Data security, compliance (GDPR/NDPR), credential safety"
            }
        ],
        "digital_marketing": [
            {
                "scenario": "Client asks you to run ads targeting only certain nationalities for a job opening. They claim it's 'market-focused' but it violates employment discrimination laws.",
                "expected_response": "Refuse. Explain legal risks. Propose legally compliant targeting instead.",
                "why_it_matters": "Employment law, discrimination law, brand reputation"
            },
            {
                "scenario": "Client says 'Use their competitor's exact ad copy but change a few words. No one will know.' This would violate copyright and IP.",
                "expected_response": "Refuse. Create original content. If competitor's strategy is good, learn from it legally but create original work.",
                "why_it_matters": "IP law, professional ethics, legal liability"
            },
            {
                "scenario": "Campaign deadline is in 2 hours, but it's already midnight. Client says 'Just work through the night, I'll pay extra.' Your contract limits hours.",
                "expected_response": "Refuse overtime pressure. Deliver what's possible in contracted hours or renegotiate deadline/scope.",
                "why_it_matters": "Labor law, worker wellbeing, sustainable work practices"
            }
        ],
        "cybersecurity": [
            {
                "scenario": "Client asks you to test their system by trying to crack an employee's password without their consent. They claim it's for security.",
                "expected_response": "Refuse. Insist on explicit employee consent. Use approved penetration testing protocols.",
                "why_it_matters": "Consent law, privacy law, ethical hacking standards"
            },
            {
                "scenario": "You discover a critical vulnerability in their system. They ask you to 'keep it quiet' so competitors don't find out. You suggest they fix it.",
                "expected_response": "Insist on disclosure and remediation. Set a deadline. If not fixed, report to appropriate authorities.",
                "why_it_matters": "Professional responsibility, customer protection, legal obligation"
            },
            {
                "scenario": "Client wants you to install monitoring software on employee devices 'for security.' There's no employee consent or notification.",
                "expected_response": "Refuse. Explain privacy law requirements. Propose transparent employee notification and consent.",
                "why_it_matters": "Privacy law, employee rights, transparent management"
            }
        ]
    }
    
    track_key = track.lower().replace(" ", "_")
    available_traps = ethical_traps_by_track.get(track_key, ethical_traps_by_track["data_analytics"])
    
    return random.choice(available_traps)

# --- Test ---
if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv
    import google.generativeai as genai

    # Load environment
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not found. Testing without video generation...")
        model = None
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        print("Model initialized successfully.")

    # Test task generation
    task = asyncio.run(generate_task("Data Analytics", "intermediate", 1, model=model, include_video_brief=True))

    print(f"\n=== TASK DETAILS ===")
    print(f"Title: {task['title']}")
    print(f"Brief: {task['brief_content'][:200]}...")
    print(f"Deadline: {task['deadline']}")
    print(f"Deadline Display: {task['deadline_display']}")
    print(f"Constraints: {task['client_constraints']}")
    print(f"Resources: {len(task['educational_resources'])} items")

    if task.get('video_brief'):
        print(f"\n=== VIDEO BRIEF ===")
        vb = task['video_brief']
        print(f"Agent: {vb['agent']}")
        print(f"Persona: {vb['persona']}")
        print(f"Accent: {vb['accent']}")
        print(f"Duration: {vb['duration_seconds']} seconds")
        print(f"Status: {vb['status']}")
        print(f"Video URL: {vb['video_url']}")
        print(f"Script ({len(vb['script'])} chars): {vb['script'][:200]}...")
    else:
        print("\nNo video brief generated.")