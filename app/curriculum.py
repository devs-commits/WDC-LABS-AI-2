"""
WDC Labs Curriculum Definitions.
Maps specific task numbers in a track to learning objectives and topics.
"""

"""
WDC Labs Curriculum Definitions.
Maps specific task numbers in a track to learning objectives and topics.
"""

CURRICULUM = {
    # ================================
    # 3A. Digital Marketing Matrix
    # ================================
    "digital_marketing": {
        1: {
            "topic": "Intro & Landscape",
            "objective": "Map the Customer Journey for a Fintech App using the '3i Principles'. Submit PDF.",
            "complexity": "Beginner",
            "key_concepts": ["customer journey map", "fintech", "3i principles", "brand awareness"]
        },
        2: {
            "topic": "SEO & AIO",
            "objective": "Audit this website. Fix 5 broken links. Rewrite meta-tags for 'AIO'. Sola checks keyword density.",
            "complexity": "Beginner",
            "key_concepts": ["SEO audit", "meta tags", "AIO", "broken links", "keyword optimization"]
        },
        3: {
            "topic": "PPC Advertising",
            "objective": "Setup $50 Google Ads Campaign (Sim). Achieve CTR > 2% or Tolu cuts budget.",
            "complexity": "Intermediate",
            "key_concepts": ["Google Ads", "CTR", "budget management", "ad copy", "keyword bidding"]
        },
        4: {
            "topic": "Display Ads",
            "objective": "Design 3 Banner Ads (Canva). Sola critiques visual hierarchy and CTA placement.",
            "complexity": "Intermediate",
            "key_concepts": ["banner ad design", "visual hierarchy", "CTA", "Canva", "brand guidelines"]
        },
        5: {
            "topic": "Email Marketing",
            "objective": "Draft a 5-part Drip sequence for Black Friday. Emem wants high open rates. No spam words.",
            "complexity": "Intermediate",
            "key_concepts": ["email drip sequence", "Black Friday strategy", "open rates", "spam triggers", "copywriting"]
        },
        6: {
            "topic": "Social & Content",
            "objective": "Create a Content Calendar for 1 month. Write 3 viral hooks. Mid-Term Reward Unlock.",
            "complexity": "Intermediate",
            "key_concepts": ["content calendar", "viral hooks", "social media strategy", "engagement"]
        },
        7: {
            "topic": "Mobile Marketing",
            "objective": "Design a Push Notification strategy. Don't be spammy. Sola will reject clickbait.",
            "complexity": "Advanced",
            "key_concepts": ["push notifications", "mobile marketing", "user retention", "anti-spam"]
        },
        8: {
            "topic": "Analytics (Basic)",
            "objective": "Traffic spiked but sales dropped. Analyze this GA4 Export. Find the leak.",
            "complexity": "Advanced",
            "key_concepts": ["GA4", "traffic analysis", "conversion funnel", "bounce rate", "data storytelling"]
        },
        9: {
            "topic": "Strategy & Planning",
            "objective": "Create a 12-month Digital Strategy for a Real Estate client. Define KPIs.",
            "complexity": "Advanced",
            "key_concepts": ["digital strategy", "KPI definition", "real estate marketing", "long-term planning"]
        },
        10: {
            "topic": "Crisis Management",
            "objective": "Twitter Crisis! 500 angry tweets. Draft a PR response strategy in 30 mins.",
            "complexity": "Advanced",
            "key_concepts": ["crisis management", "PR strategy", "social listening", "brand reputation"]
        },
        11: {
            "topic": "Capstone Prep",
            "objective": "Compile your Live Portfolio. Tolu reviews your Case Studies.",
            "complexity": "Advanced",
            "key_concepts": ["portfolio building", "case study writing", "personal branding", "presentation"]
        },
        12: {
            "topic": "Boardroom Defense",
            "objective": "Present Strategy to Client. Defend your ROAS projections.",
            "complexity": "Expert",
            "key_concepts": ["strategy presentation", "ROAS defense", "client communication", "public speaking"]
        }
    },

    # ================================
    # 3B. Data Analytics Matrix
    # ================================
    "data_analytics": {
        1: {
            "topic": "Excel Core",
            "objective": "Clean messy sales log using XLOOKUP. No VLOOKUP allowed.",
            "complexity": "Beginner",
            "key_concepts": ["Excel data cleaning", "XLOOKUP", "data validation", "formatting"]
        },
        2: {
            "topic": "Excel Viz",
            "objective": "Create Dashboard via Power Query. Do not copy-paste data.",
            "complexity": "Beginner",
            "key_concepts": ["Power Query", "Excel dashboard", "data transformation", "charts"]
        },
        3: {
            "topic": "Excel Project",
            "objective": "Retail Dataset Analysis. Create User Story.",
            "complexity": "Intermediate",
            "key_concepts": ["retail analysis", "user stories", "business insights", "data storytelling"]
        },
        4: {
            "topic": "SQL Basics",
            "objective": "Write query to find top 5 customers. Server crash risk if slow.",
            "complexity": "Intermediate",
            "key_concepts": ["SQL SELECT", "ORDER BY", "LIMIT", "performance optimization"]
        },
        5: {
            "topic": "Advanced SQL",
            "objective": "Clean 'User_ID' column (CAST/REPLACE). Join with 'Orders'.",
            "complexity": "Intermediate",
            "key_concepts": ["SQL JOINS", "CAST", "REPLACE", "data cleaning in SQL"]
        },
        6: {
            "topic": "SQL Project",
            "objective": "Banking DB Analysis. Submit SQL Script. Mid-Term Reward Unlock.",
            "complexity": "Intermediate",
            "key_concepts": ["banking data analysis", "complex queries", "database schema", "SQL scripting"]
        },
        7: {
            "topic": "Power BI Core",
            "objective": "Import 3 CSVs. Create DAX measure for 'MoM Growth'.",
            "complexity": "Advanced",
            "key_concepts": ["Power BI data modeling", "DAX", "MoM growth", "measure creation"]
        },
        8: {
            "topic": "Power BI Viz",
            "objective": "Build Q3 Executive Dashboard. Publish to Web.",
            "complexity": "Advanced",
            "key_concepts": ["executive dashboard", "Power BI publishing", "interactive visualization", "KPIs"]
        },
        9: {
            "topic": "Python Basics",
            "objective": "Load 2GB file with Pandas. Excel failed. Group by 'Region'.",
            "complexity": "Advanced",
            "key_concepts": ["Pandas", "large datasets", "groupby", "Python for data"]
        },
        10: {
            "topic": "Python Viz",
            "objective": "Visualize Ad Spend vs Sales using Seaborn.",
            "complexity": "Advanced",
            "key_concepts": ["Seaborn", "data visualization", "correlation analysis", "Python plotting"]
        },
        11: {
            "topic": "Real World",
            "objective": "Legacy Repo Fix. Debug the previous intern's Python script.",
            "complexity": "Advanced",
            "key_concepts": ["debugging", "legacy code", "code review", "Python scripting"]
        },
        12: {
            "topic": "Boardroom Defense",
            "objective": "Defend Python vs SQL choice to the CTO (Sola).",
            "complexity": "Expert",
            "key_concepts": ["technical decision making", "tool selection logic", "communication", "CTO defense"]
        }
    },

    # ================================
    # 3C. Cybersecurity Matrix
    # ================================
    "cybersecurity": {
        1: {
            "topic": "Linux Basics",
            "objective": "Server down. SSH in. Navigate via CLI only. No GUI.",
            "complexity": "Beginner",
            "key_concepts": ["Linux CLI", "SSH", "file navigation", "troubleshooting"]
        },
        2: {
            "topic": "Attacks",
            "objective": "Mastercard Log Analysis. Identify DDoS vs Brute Force.",
            "complexity": "Beginner",
            "key_concepts": ["log analysis", "DDoS", "Brute Force", "incident identification"]
        },
        3: {
            "topic": "Sec Fundamentals",
            "objective": "Audit User Permissions. Remove 'Intern' Admin access.",
            "complexity": "Intermediate",
            "key_concepts": ["user permissions", "IAM", "least privilege", "access audit"]
        },
        4: {
            "topic": "Network Sec",
            "objective": "Clifford Chance Firewall Config. Block non-SSL traffic.",
            "complexity": "Intermediate",
            "key_concepts": ["firewall rules", "SSL/TLS", "network traffic control", "security configuration"]
        },
        5: {
            "topic": "Host/Data Sec",
            "objective": "Encrypt sensitive client file (AES-256). Verify Hash.",
            "complexity": "Intermediate",
            "key_concepts": ["encryption", "AES-256", "hashing", "data integrity"]
        },
        6: {
            "topic": "Network Services",
            "objective": "PWC Audit. Nmap scan for open ports. Mid-Term Reward.",
            "complexity": "Intermediate",
            "key_concepts": ["Nmap", "port scanning", "vulnerability assessment", "network audit"]
        },
        7: {
            "topic": "Authentication",
            "objective": "Implement MFA logic. Test for bypass vulnerabilities.",
            "complexity": "Advanced",
            "key_concepts": ["MFA implementation", "authentication security", "vulnerability testing", "bypass techniques"]
        },
        8: {
            "topic": "Access/Crypto",
            "objective": "Datacom Breach. Decrypt intercepted message with private key.",
            "complexity": "Advanced",
            "key_concepts": ["cryptography", "private/public keys", "decryption", "incident response"]
        },
        9: {
            "topic": "Org Security",
            "objective": "Draft Disaster Recovery Policy. Define RTO/RPO.",
            "complexity": "Advanced",
            "key_concepts": ["disaster recovery", "policy writing", "RTO/RPO", "business continuity"]
        },
        10: {
            "topic": "Disaster Recovery",
            "objective": "Ransomware Sim. Isolate host. Restore from Backup.",
            "complexity": "Advanced",
            "key_concepts": ["ransomware response", "containment", "backup restoration", "incident simulation"]
        },
        11: {
            "topic": "Capstone Prep",
            "objective": "Compile Vulnerability Reports into Portfolio.",
            "complexity": "Advanced",
            "key_concepts": ["reporting", "vulnerability management", "portfolio creation", "technical writing"]
        },
        12: {
            "topic": "Boardroom Defense",
            "objective": "Defend your Patch Strategy to the Board.",
            "complexity": "Expert",
            "key_concepts": ["executive communication", "patch management strategy", "risk communication", "board defense"]
        }
    }
}


def get_curriculum_step(track: str, task_number: int):
    """Retrieve the specific curriculum step for a given track and task number."""
    track_key = track.lower().replace(" ", "_")
    track_curriculum = CURRICULUM.get(track_key, {})
    return track_curriculum.get(task_number)
