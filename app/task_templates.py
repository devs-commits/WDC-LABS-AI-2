"""
WDC Labs Task Templates
Library of "Ungoogleable" task templates with messy data generation.
Includes ethical training scenarios and compliance checks.
"""

import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.utils.deadline_formatter import format_deadline_display

# --- Industry contexts for task variation ---
INDUSTRIES = [
    "Fintech", "Agriculture", "Logistics", "Healthcare", "E-commerce",
    "Real Estate", "Education", "Energy", "Hospitality", "Manufacturing"
]

# --- Nigerian cities for localized context ---
NIGERIAN_CITIES = [
    "Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan",
    "Kaduna", "Benin City", "Enugu", "Warri", "Ilorin"
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
    "data_analytics": [
        {
            "title_template": "Data Cleansing: {company} Sales Data",
            "brief_template": """
Here is a CSV file containing sales data for {company} for {month} {year}. 
There are {anomaly_count} anomalies in the dataset caused by {error_cause}.
Find them and calculate the real ROAS.

**Requirements:**
- Identify all anomalies
- Document what was wrong with each
- Calculate corrected ROAS (Return on Ad Spend)
- Provide a 3-sentence summary of findings
""",
            "constraints": "Must use Python. No external libraries except pandas and numpy.",
            "difficulty_levels": ["beginner", "intermediate", "advanced"]
        },
        {
            "title_template": "{company} Customer Segmentation Analysis",
            "brief_template": """
The marketing team at {company} needs to understand their customer base better.
Analyze the provided dataset and create customer segments based on:
- Purchase frequency
- Average order value
- Time since last purchase

**Deliverables:**
1. At least 3 distinct customer segments
2. Characteristics of each segment
3. One marketing recommendation per segment
""",
            "constraints": "Analysis must be reproducible. Document your methodology.",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ],
    
    "digital_marketing": [
        {
            "title_template": "SEO Audit: {company} Website",
            "brief_template": """
Conduct a comprehensive SEO audit for {company}'s website.
The client is in the {industry} industry and targeting the {city} market.

**Audit Scope:**
1. Technical SEO issues (at least 5)
2. On-page optimization opportunities
3. Content gap analysis
4. 3 competitor keywords they should target

**Note:** The website has some intentional errors. Find them.
""",
            "constraints": "Use only free tools. Screaming Frog free version is acceptable.",
            "difficulty_levels": ["beginner", "intermediate"]
        },
        {
            "title_template": "Social Media Campaign: {company} Product Launch",
            "brief_template": """
{company} is launching a new product next month. Create a 2-week social media campaign.

**Requirements:**
- Content calendar with specific post ideas
- Platform-specific strategies (Instagram, Twitter, LinkedIn)
- Hashtag strategy
- KPIs to track success

**Constraint:** Budget is ₦50,000 for the entire campaign.
""",
            "constraints": "All content must be culturally appropriate for Nigerian audience.",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ],
    
    "cybersecurity": [
        {
            "title_template": "Vulnerability Assessment: {company} Network",
            "brief_template": """
You've been engaged to assess the security posture of {company}'s network.
Review the provided network diagram and configuration files.

**Identify:**
1. At least 3 security vulnerabilities
2. Risk level for each (High/Medium/Low)
3. Remediation steps
4. Quick wins vs. long-term fixes

**Note:** The configs contain some common misconfigurations. Document them.
""",
            "constraints": "Do not attempt active scanning. This is a passive assessment only.",
            "difficulty_levels": ["beginner", "intermediate", "advanced"]
        },
        {
            "title_template": "Security Policy Review: {company}",
            "brief_template": """
{company} just received their information security policy from legal.
Review the document for gaps and weaknesses.

**Focus Areas:**
1. Password policy adequacy
2. Incident response procedures
3. Data classification gaps
4. Access control weaknesses

Provide specific recommendations with priority rankings.
""",
            "constraints": "Recommendations must be practical for a small business (under 50 employees).",
            "difficulty_levels": ["intermediate", "advanced"]
        }
    ]
}

# --- Resource Content Library (Markdown) ---
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
    
    for item in ARCHIVE_LIBRARY.get(track, []):
        if any(tag in task_lower for tag in item["tags"]):
            resources.append(item)
    
    # Always add a general reference hint
    resources += ARCHIVE_LIBRARY.get("general", [])[:1]
    
    return resources[:3]  # max 3 resources

# --- Main task generation function ---
def generate_task(
    track: str,
    difficulty: str = "intermediate",
    task_number: int = 1,
    user_city: str = None,
    include_ethical_trap: bool = None,
    user_name: str = "Intern",
    model = None
) -> Dict[str, Any]:
    """
    Generate a unique, ungoogleable task based on track and difficulty.
    20-30% of tasks include ethical traps to test professional judgment.
    """

    # Normalize track name
    track_key = track.lower().replace(" ", "_")
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
        Generate a detailed task brief for an intern named "{user_name}" at a {industry} company named {company}.
        
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
        
        **Output Format (JSON):**
        {{
            "title": "Professional Task Title",
            "brief_template": "Full markdown brief...",
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
                 
        except Exception as e:
            print(f"Curriculum generation failed: {e}. Falling back to curriculum-static mode.")
            # Fallback to Curriculum Static Mode (prevents random tasks)
            title = f"{curriculum['topic']}: {company}"
            brief = f"""
**Topic:** {curriculum['topic']}
**Objective:** {curriculum['objective']}

**Context:**
Dear {user_name},
You are working at {company} in {city}.
The manager needs you to complete the objective above.

**Key Concepts:**
- {', '.join(curriculum['key_concepts'])}

**Instructions:**
Complete the objective using the tools provided.
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
    
    # deadline - 1 day
    duration_days = 1
    deadline = now + timedelta(days=duration_days)
    deadline_display = format_deadline_display(deadline.isoformat())

    # --- Resource selection ---

    # --- Resource selection ---
    # Pick relevant metadata first
    resource_metadata = select_task_resources(brief, track_key)
    
    educational_resources = []
    
    # If model is available, use AI to generate the content dynamically
    if model:
        for meta in resource_metadata:
            try:
                # Generate dynamic content based on title, brief, and industry context
                prompt = f"""
                Create a practical, short "Cheat Sheet" or "Guide" for an intern working on this task:
                
                Task: {title}
                Industry: {industry}
                Topic: {meta['title']}
                Tags: {meta['tags']}
                
                The content should be in Markdown format.
                Include code snippets (if technical), checklists, or step-by-step instructions.
                Keep it under 300 words. Make it look like a real internal document.
                """
                
                response = model.generate_content(prompt)
                content = response.text
                
                educational_resources.append({
                    "title": meta["title"],
                    "description": f"AI-Generated Resource for {company}",
                    "content": content
                })
            except Exception as e:
                print(f"Error generating resource content: {e}")
                # Fallback to static content
                educational_resources.append({
                    "title": meta["title"],
                    "description": f"Internal Resource ({meta['id']})",
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
        "educational_resources": educational_resources
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
    task = generate_task("Data Analytics", "intermediate", 1)
    print(f"Title: {task['title']}")
    print(f"Brief: {task['brief_content'][:200]}...")
    print(f"Constraints: {task['client_constraints']}")
    print(f"Resources: {task['educational_resources']}")