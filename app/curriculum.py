"""
WDC Labs Curriculum Definitions.
Maps specific task numbers in a track to learning objectives, topics, and gamification badges.
"""
import datetime

FRAMEWORK_DEFINITIONS = {
    "3i_principles": "Initiate, Iterate, Integrate"
}

# ============================================================
# 24-WEEK GAMIFIED PROGRESSION IDENTITY ENGINE
# ============================================================

def get_identity_for_week(track: str, week: int) -> str:
    """Dynamically maps the user's week to their gamified job title."""
    
    # Normalize the track string to ensure it perfectly matches our dictionary
    track_key = track.lower().replace(" ", "_").replace("-", "_")

    if track_key == "data_analytics":
        if week <= 4: return "Data Intern"
        if week <= 8: return "Junior Data Analyst"
        if week <= 12: return "Data Analyst"
        if week <= 16: return "Business Intelligence Analyst"
        if week <= 20: return "Analytics Strategist"
        return "Director of Analytics"

    elif track_key == "digital_marketing":
        if week <= 4: return "Marketing Intern"
        if week <= 8: return "Campaign Operator"
        if week <= 12: return "Digital Marketing Associate"
        if week <= 16: return "Performance Marketer"
        if week <= 20: return "Growth Strategist"
        return "Marketing Director"

    elif track_key == "cyber_security":
        if week <= 4: return "Security Intern"
        if week <= 8: return "Security Associate"
        if week <= 12: return "Security Analyst"
        if week <= 16: return "Threat Defender"
        if week <= 20: return "Incident Commander"
        return "Chief Security Strategist"
    
    return "Intern"


# ============================================================
# MASTER 24-WEEK CURRICULUM & BADGE MAPPING
# ============================================================

CURRICULUM = {
    # ================================
    # DIGITAL MARKETING MATRIX
    # ================================
    "digital_marketing": {
        1: {"topic": "Intro to Digital Marketing", "objective": "Understand the digital marketing ecosystem and how businesses grow online.", "complexity": "Beginner", "key_concepts": ["ecosystem", "business growth"], "badge_opportunity": None},
        2: {"topic": "Customer Journey & Psychology", "objective": "Learn buyer behavior, personas, funnels, and the 3i Principles.", "complexity": "Beginner", "key_concepts": ["buyer behavior", "funnels", "3i Principles"], "badge_opportunity": "Audience Analyst"},
        3: {"topic": "Content & Social Media Basics", "objective": "Learn content strategy, hooks, engagement, and platform behavior.", "complexity": "Beginner", "key_concepts": ["content strategy", "engagement"], "badge_opportunity": "Content Operator"},
        4: {"topic": "SEO & Search Fundamentals", "objective": "Understand search intent, discoverability, and on-page SEO.", "complexity": "Intermediate", "key_concepts": ["SEO", "search intent"], "badge_opportunity": "SEO Explorer"},
        5: {"topic": "Meta Ads Fundamentals", "objective": "Learn campaign objectives, audience targeting, and ad structures.", "complexity": "Intermediate", "key_concepts": ["Meta Ads", "targeting"], "badge_opportunity": None},
        6: {"topic": "Google Ads & PPC", "objective": "Learn search advertising, keyword intent, and bidding strategies.", "complexity": "Intermediate", "key_concepts": ["Google Ads", "PPC", "bidding"], "badge_opportunity": "Paid Media Operator"},
        7: {"topic": "Creatives & Landing Pages", "objective": "Learn conversion-focused copywriting, visuals, and CTAs.", "complexity": "Intermediate", "key_concepts": ["copywriting", "landing pages"], "badge_opportunity": None},
        8: {"topic": "Email & Mobile Marketing", "objective": "Learn lifecycle marketing and customer retention systems.", "complexity": "Intermediate", "key_concepts": ["email marketing", "retention"], "badge_opportunity": None},
        9: {"topic": "Analytics & Tracking", "objective": "Learn attribution, KPIs, GA4, Meta Pixel, and tracking systems.", "complexity": "Advanced", "key_concepts": ["GA4", "Meta Pixel", "attribution"], "badge_opportunity": None},
        10: {"topic": "Media Planning & Strategy", "objective": "Learn budgeting, KPI planning, and channel allocation.", "complexity": "Advanced", "key_concepts": ["budgeting", "media planning"], "badge_opportunity": None},
        11: {"topic": "Campaign Optimization", "objective": "Learn testing, scaling, creative fatigue, and ROAS improvement.", "complexity": "Advanced", "key_concepts": ["ROAS", "scaling", "optimization"], "badge_opportunity": "Optimization Expert"},
        12: {"topic": "Portfolio + Boardroom Defense", "objective": "Learn reporting, presentation, and client communication skills.", "complexity": "Expert", "key_concepts": ["reporting", "client communication"], "badge_opportunity": None},
        13: {"topic": "Advanced Meta Ads", "objective": "Learn retargeting, CBO, lookalikes, and scaling systems.", "complexity": "Expert", "key_concepts": ["CBO", "lookalikes", "retargeting"], "badge_opportunity": None},
        14: {"topic": "Advanced Google Ads", "objective": "Learn PMAX, YouTube Ads, Display Ads, and advanced optimization.", "complexity": "Expert", "key_concepts": ["PMAX", "YouTube Ads"], "badge_opportunity": None},
        15: {"topic": "Conversion Rate Optimization (CRO)", "objective": "Learn heatmaps, A/B testing, and user behavior optimization.", "complexity": "Expert", "key_concepts": ["CRO", "A/B testing"], "badge_opportunity": None},
        16: {"topic": "Full Funnel Systems", "objective": "Learn multi-touch attribution and acquisition-to-retention systems.", "complexity": "Expert", "key_concepts": ["multi-touch attribution", "funnels"], "badge_opportunity": "Funnel Builder"},
        17: {"topic": "Advanced Analytics", "objective": "Learn attribution models, cohorts, CAC, and customer LTV.", "complexity": "Expert", "key_concepts": ["CAC", "LTV", "cohorts"], "badge_opportunity": "Analytics Specialist"},
        18: {"topic": "Marketing Automation", "objective": "Learn CRM workflows, automation systems, and lead nurturing.", "complexity": "Expert", "key_concepts": ["CRM", "lead nurturing"], "badge_opportunity": None},
        19: {"topic": "Growth Marketing Systems", "objective": "Learn experimentation frameworks and Pirate Metrics.", "complexity": "Expert", "key_concepts": ["Pirate Metrics", "experimentation"], "badge_opportunity": "Growth Strategist"},
        20: {"topic": "AI in Marketing", "objective": "Learn AI-assisted workflows, prompting, and automation tools.", "complexity": "Expert", "key_concepts": ["AI tools", "automation"], "badge_opportunity": None},
        21: {"topic": "Crisis & Reputation Management", "objective": "Learn PR response, brand recovery, and communication under pressure.", "complexity": "Expert", "key_concepts": ["PR response", "reputation management"], "badge_opportunity": "Crisis Manager"},
        22: {"topic": "Client & Stakeholder Management", "objective": "Learn reporting, negotiation, and expectation management.", "complexity": "Expert", "key_concepts": ["negotiation", "expectation management"], "badge_opportunity": None},
        23: {"topic": "Agency Simulation", "objective": "Learn collaboration, prioritization, and campaign operations.", "complexity": "Expert", "key_concepts": ["campaign operations", "prioritization"], "badge_opportunity": None},
        24: {"topic": "Executive Boardroom Defense", "objective": "Learn leadership communication and strategic decision-making.", "complexity": "Expert", "key_concepts": ["leadership", "decision-making"], "badge_opportunity": "Boardroom Certified"}
    },

    # ================================
    # DATA ANALYTICS MATRIX
    # ================================
    "data_analytics": {
        1: {"topic": "Intro to Data Analytics", "objective": "Understand what data analysts do and how businesses use data.", "complexity": "Beginner", "key_concepts": ["business logic", "patterns"], "badge_opportunity": None},
        2: {"topic": "Excel Basics", "objective": "Learn spreadsheets, formatting, sorting, and filtering confidently.", "complexity": "Beginner", "key_concepts": ["Excel", "filtering", "formatting"], "badge_opportunity": "Spreadsheet Survivor"},
        3: {"topic": "Excel Functions & Formulas", "objective": "Learn formulas and data cleaning workflows.", "complexity": "Beginner", "key_concepts": ["IF", "SUMIF", "COUNTIF"], "badge_opportunity": "Formula Operator"},
        4: {"topic": "Data Visualization in Excel", "objective": "Learn charts, dashboards, and storytelling basics.", "complexity": "Beginner", "key_concepts": ["dashboards", "charts"], "badge_opportunity": None},
        5: {"topic": "Power Query & Data Cleaning", "objective": "Learn transformation and structured cleaning workflows.", "complexity": "Intermediate", "key_concepts": ["Power Query", "transformation"], "badge_opportunity": None},
        6: {"topic": "Excel Business Project", "objective": "Apply Excel knowledge to solve business problems.", "complexity": "Intermediate", "key_concepts": ["business recommendations", "retail data"], "badge_opportunity": "Insight Hunter"},
        7: {"topic": "SQL Basics", "objective": "Learn databases, SELECT statements, filtering, and sorting.", "complexity": "Intermediate", "key_concepts": ["SQL", "SELECT", "filtering"], "badge_opportunity": "SQL Investigator"},
        8: {"topic": "SQL Joins & Aggregation", "objective": "Learn joins, grouping, and business analysis queries.", "complexity": "Intermediate", "key_concepts": ["JOIN", "GROUP BY"], "badge_opportunity": None},
        9: {"topic": "Intermediate SQL Analysis", "objective": "Learn analytical SQL workflows.", "complexity": "Advanced", "key_concepts": ["sales trends", "SQL workflows"], "badge_opportunity": None},
        10: {"topic": "Power BI Fundamentals", "objective": "Learn dashboarding and business intelligence basics.", "complexity": "Advanced", "key_concepts": ["Power BI", "KPI cards"], "badge_opportunity": "Dashboard Specialist"},
        11: {"topic": "Power BI Dashboards & DAX", "objective": "Learn advanced dashboards and executive reporting.", "complexity": "Advanced", "key_concepts": ["DAX", "executive reporting"], "badge_opportunity": None},
        12: {"topic": "Portfolio + Analyst Defense", "objective": "Learn reporting and stakeholder communication.", "complexity": "Expert", "key_concepts": ["stakeholder defense", "insights"], "badge_opportunity": None},
        13: {"topic": "Python for Data Analytics", "objective": "Learn Python fundamentals using business datasets.", "complexity": "Expert", "key_concepts": ["Python", "Pandas", "CSV"], "badge_opportunity": None},
        14: {"topic": "Data Manipulation with Pandas", "objective": "Learn filtering, grouping, merging, and transformations.", "complexity": "Expert", "key_concepts": ["Pandas", "data manipulation"], "badge_opportunity": None},
        15: {"topic": "Python Visualization", "objective": "Learn Matplotlib and Seaborn for storytelling.", "complexity": "Expert", "key_concepts": ["Matplotlib", "Seaborn"], "badge_opportunity": None},
        16: {"topic": "Working with Big Data Files", "objective": "Learn efficient workflows for large datasets.", "complexity": "Expert", "key_concepts": ["big data", "efficiency"], "badge_opportunity": None},
        17: {"topic": "Statistical Analysis", "objective": "Learn averages, variance, correlations, and forecasting basics.", "complexity": "Expert", "key_concepts": ["variance", "correlations", "forecasting"], "badge_opportunity": None},
        18: {"topic": "Advanced Power BI & DAX", "objective": "Learn advanced reporting logic and automation.", "complexity": "Expert", "key_concepts": ["DAX", "drill-down analysis"], "badge_opportunity": None},
        19: {"topic": "Business Reporting & Communication", "objective": "Learn insight presentation and stakeholder reporting.", "complexity": "Expert", "key_concepts": ["boardroom reporting", "communication"], "badge_opportunity": "Data Storyteller"},
        20: {"topic": "Analytics Automation", "objective": "Learn scheduled reporting and automated workflows.", "complexity": "Expert", "key_concepts": ["automation", "scheduled reporting"], "badge_opportunity": "Automation Specialist"},
        21: {"topic": "Predictive Analytics Foundations", "objective": "Learn trend forecasting and predictive thinking.", "complexity": "Expert", "key_concepts": ["predictive analytics", "forecasting"], "badge_opportunity": "Predictive Analyst"},
        22: {"topic": "Cross-Department Data Analysis", "objective": "Learn collaborative business analytics workflows.", "complexity": "Expert", "key_concepts": ["cross-department", "revenue leakage"], "badge_opportunity": None},
        23: {"topic": "Real-World Data Crisis Simulation", "objective": "Learn debugging and operational analytics pressure handling.", "complexity": "Expert", "key_concepts": ["debugging", "crisis handling"], "badge_opportunity": "Crisis Analyst"},
        24: {"topic": "Boardroom Defense & Strategic Analytics", "objective": "Learn leadership communication and strategic insight defense.", "complexity": "Expert", "key_concepts": ["strategy", "executive leadership"], "badge_opportunity": "Executive Analyst"}
    },

    # ================================
    # CYBER SECURITY MATRIX
    # ================================
    "cyber_security": {
        1: {"topic": "Intro to Cybersecurity", "objective": "Understand cybersecurity, digital threats, and business risks.", "complexity": "Beginner", "key_concepts": ["phishing", "threats", "business risk"], "badge_opportunity": None},
        2: {"topic": "Linux & Command Line Basics", "objective": "Build confidence navigating systems using CLI.", "complexity": "Beginner", "key_concepts": ["CLI", "directories", "permissions"], "badge_opportunity": "Linux Operator"},
        3: {"topic": "Networking Fundamentals", "objective": "Learn how systems communicate and exchange data.", "complexity": "Beginner", "key_concepts": ["TCP/IP", "DNS", "packet tracing"], "badge_opportunity": None},
        4: {"topic": "Security Fundamentals", "objective": "Learn authentication, permissions, and access control.", "complexity": "Intermediate", "key_concepts": ["IAM", "authentication", "access control"], "badge_opportunity": None},
        5: {"topic": "Firewalls & Network Security", "objective": "Learn traffic filtering and secure configurations.", "complexity": "Intermediate", "key_concepts": ["firewall rules", "port filtering"], "badge_opportunity": "Network Defender"},
        6: {"topic": "Threats & Vulnerabilities", "objective": "Learn attack types and detection methods.", "complexity": "Intermediate", "key_concepts": ["DDoS", "brute-force", "log analysis"], "badge_opportunity": "Threat Hunter"},
        7: {"topic": "Authentication & MFA", "objective": "Learn identity protection and MFA systems.", "complexity": "Advanced", "key_concepts": ["MFA", "identity protection"], "badge_opportunity": None},
        8: {"topic": "Encryption & Cryptography", "objective": "Learn hashing, encryption, and data integrity.", "complexity": "Advanced", "key_concepts": ["hashing", "encryption"], "badge_opportunity": "Encryption Specialist"},
        9: {"topic": "Monitoring & Incident Response", "objective": "Learn operational monitoring and response workflows.", "complexity": "Advanced", "key_concepts": ["vulnerability scans", "monitoring"], "badge_opportunity": None},
        10: {"topic": "Disaster Recovery Fundamentals", "objective": "Learn business continuity and recovery planning.", "complexity": "Advanced", "key_concepts": ["ransomware", "disaster recovery"], "badge_opportunity": "Incident Responder"},
        11: {"topic": "Security Reporting & Documentation", "objective": "Learn professional reporting and portfolio preparation.", "complexity": "Advanced", "key_concepts": ["reporting", "vulnerability documentation"], "badge_opportunity": None},
        12: {"topic": "Boardroom Defense & Risk Communication", "objective": "Learn stakeholder communication and strategic defense.", "complexity": "Expert", "key_concepts": ["risk mitigation", "stakeholder communication"], "badge_opportunity": None},
        13: {"topic": "Advanced Network Security", "objective": "Learn IDS/IPS systems and secure architectures.", "complexity": "Expert", "key_concepts": ["IDS/IPS", "secure architectures"], "badge_opportunity": None},
        14: {"topic": "Ethical Hacking Fundamentals", "objective": "Learn penetration testing concepts safely.", "complexity": "Expert", "key_concepts": ["pentesting", "vulnerability scanning"], "badge_opportunity": "Vulnerability Analyst"},
        15: {"topic": "Web Application Security", "objective": "Learn OWASP Top 10 vulnerabilities and prevention.", "complexity": "Expert", "key_concepts": ["OWASP", "web vulnerabilities"], "badge_opportunity": None},
        16: {"topic": "Device & Endpoint Protection", "objective": "Learn endpoint monitoring and malware defense.", "complexity": "Expert", "key_concepts": ["endpoint monitoring", "malware defense"], "badge_opportunity": None},
        17: {"topic": "Cloud & Infrastructure Security", "objective": "Learn cloud security concepts and configurations.", "complexity": "Expert", "key_concepts": ["cloud security", "storage buckets"], "badge_opportunity": None},
        18: {"topic": "SOC Workflows & Threat Hunting", "objective": "Learn SOC operations and threat detection.", "complexity": "Expert", "key_concepts": ["SOC", "threat hunting"], "badge_opportunity": "SOC Operator"},
        19: {"topic": "Security Policies & Compliance", "objective": "Learn governance, risk, and compliance frameworks.", "complexity": "Expert", "key_concepts": ["governance", "compliance"], "badge_opportunity": "Compliance Guardian"},
        20: {"topic": "Security Automation & AI Risks", "objective": "Learn automated defense systems and AI threats.", "complexity": "Expert", "key_concepts": ["automation", "AI threats"], "badge_opportunity": None},
        21: {"topic": "Enterprise Incident Management", "objective": "Learn coordinated enterprise-level response workflows.", "complexity": "Expert", "key_concepts": ["enterprise breach", "coordination"], "badge_opportunity": "Crisis Commander"},
        22: {"topic": "Attack & Defense Simulation", "objective": "Learn offensive vs defensive operations.", "complexity": "Expert", "key_concepts": ["attack simulation", "defense operations"], "badge_opportunity": None},
        23: {"topic": "Security Operations Management", "objective": "Learn prioritization, escalation, and team workflows.", "complexity": "Expert", "key_concepts": ["prioritization", "escalation"], "badge_opportunity": None},
        24: {"topic": "Executive Boardroom Defense", "objective": "Learn strategic cybersecurity communication and leadership.", "complexity": "Expert", "key_concepts": ["strategy", "leadership"], "badge_opportunity": "Cyber Defense Certified"}
    }
}

def get_curriculum_step(track: str, task_number: int):
    """
    Retrieve the specific curriculum step for a given track and task number.
    Injects dynamic gamification identity based on the task_number (week).
    """
    track_key = track.lower().replace(" ", "_").replace("-", "_")
    track_curriculum = CURRICULUM.get(track_key, {})
    
    step_data = track_curriculum.get(task_number)
    
    if step_data:
        # Dynamically inject the job title they hold during this specific week
        step_data["current_identity"] = get_identity_for_week(track_key, task_number)
        
    print(f"fetched curriculum step for {track_key} week {task_number}: -->", step_data)
    return step_data


# ============================================================
# PROGRESSION & BADGE ENGINE
# ============================================================

def process_task_completion(supabase_client, user_id, track: str, completed_week: int):
    """
    IMPORTANT: Do NOT call this inside emem.py. 
    Call this function from your API Route or Orchestrator exactly where you run the code 
    that marks the task as 'completed' in the database.
    """
    track_key = track.lower().replace(" ", "_").replace("-", "_")
    
    # 1. Calculate new identity
    new_identity = get_identity_for_week(track_key, completed_week)
    
    # 2. Update user_progression table
    progression_data = {
        "user_id": user_id,
        "current_week": completed_week,
        "current_identity": new_identity,
        "week_status": "passed_waiting",
        "updated_at": datetime.datetime.utcnow().isoformat()
    }
    
    supabase_client.table("user_progression").upsert(
        progression_data
    ).execute()
    
    # 3. Automatically award a badge if this week has one!
    curriculum_step = CURRICULUM.get(track_key, {}).get(completed_week, {})
    badge_to_award = curriculum_step.get("badge_opportunity")
    
    if badge_to_award:
        badge_data = {
            "user_id": user_id,
            "badge_name": badge_to_award,
            "earned_in_week": completed_week
        }
        try:
            supabase_client.table("user_badges").insert(badge_data).execute()
            print(f"🎉 Successfully awarded '{badge_to_award}' badge to user {user_id}!")
        except Exception as e:
            print(f"User {user_id} already has badge '{badge_to_award}' or an error occurred: {e}")