"""
WDC Labs Task Templates
Library of "Ungoogleable" task templates with messy data generation.
"""

import random
from typing import List, Dict, Any
from datetime import datetime, timedelta


# Industry contexts for task variation
INDUSTRIES = [
    "Fintech", "Agriculture", "Logistics", "Healthcare", "E-commerce",
    "Real Estate", "Education", "Energy", "Hospitality", "Manufacturing"
]

# Nigerian cities for localized context
NIGERIAN_CITIES = [
    "Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan",
    "Kaduna", "Benin City", "Enugu", "Warri", "Ilorin"
]

# Company name generators
COMPANY_PREFIXES = ["Tech", "Smart", "Prime", "Nova", "Apex", "Swift", "Core", "Global"]
COMPANY_SUFFIXES = ["Hub", "Labs", "Solutions", "Systems", "Ventures", "Group", "Corp"]


def generate_company_name(industry: str) -> str:
    """Generate a random but realistic company name."""
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    city = random.choice(NIGERIAN_CITIES)
    return f"{city} {prefix} {suffix}"


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
    for i in range(anomaly_count):
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


# Task templates by track
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


def generate_task(
    track: str,
    difficulty: str = "intermediate",
    task_number: int = 1,
    user_city: str = None,
    user_country: str = None
) -> Dict[str, Any]:
    """
    Generate a unique, ungoogleable task based on track and difficulty.
    """
    # Normalize track name
    track_key = track.lower().replace(" ", "_")
    if track_key not in TASK_TEMPLATES:
        track_key = "data_analytics"  # Default
    
    # Filter templates by difficulty
    available_templates = [
        t for t in TASK_TEMPLATES[track_key]
        if difficulty.lower() in t.get("difficulty_levels", ["intermediate"])
    ]
    
    if not available_templates:
        available_templates = TASK_TEMPLATES[track_key]
    
    template = random.choice(available_templates)
    
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
    title = template["title_template"].format(
        company=company,
        industry=industry,
        city=city
    )
    
    brief = template["brief_template"].format(
        company=company,
        industry=industry,
        city=city,
        month=month,
        year=year,
        anomaly_count=random.randint(2, 5),
        error_cause=random.choice(error_causes)
    )
    
    # Calculate deadline based on difficulty
    NEXT_DAY = 1
    deadline = now + timedelta(days=NEXT_DAY)

    
    return {
        "title": title,
        "brief_content": brief.strip(),
        "difficulty": difficulty,
        "client_constraints": template.get("constraints"),
        "attachments": [],  # Would generate/attach files in production
        "ai_persona_config": {
            "role": "Supervisor",
            "tone": "professional",
            "expertise": track,
            "instruction": "Review submission thoroughly",
            "duration": f"{deadline_days.get(difficulty, 2)} days"
        },
        "metadata": {
            "company": company,
            "industry": industry,
            "city": city,
            "task_number": task_number
        }
    }


# Test
if __name__ == "__main__":
    task = generate_task("Data Analytics", "intermediate", 1)
    print(f"Title: {task['title']}")
    print(f"Brief: {task['brief_content'][:200]}...")
    print(f"Constraints: {task['client_constraints']}")
