"""
WDC Labs Curriculum Definitions.
Maps specific task numbers in a track to learning objectives and topics.
"""

FRAMEWORK_DEFINITIONS = {
    "3i_principles": "Initiate, Iterate, Integrate"
}

CURRICULUM = {
    # ================================
    # 3A. Digital Marketing Matrix
    # ================================
    "digital_marketing": {
        1: {
            "topic": "Intro to Digital Marketing",
            "objective": "Understand how digital marketing works as a business growth system. Reality Task: Analyze how a local business attracts customers online. Identify their channels.",
            "complexity": "Beginner",
            "key_concepts": ["digital marketing basics", "channel identification", "business growth"]
        },
        2: {
            "topic": "Customer Journey & Marketing Psychology",
            "objective": "Learn audience behavior, funnels, and messaging basics. Reality Task: Map the customer journey for a fintech app using the 3i Principles.",
            "complexity": "Beginner",
            "key_concepts": ["customer journey", "3i principles", "marketing psychology", "funnels"]
        },
        3: {
            "topic": "Content & Social Media Basics",
            "objective": "Learn content strategy, hooks, and engagement. Reality Task: Create 1 week of Instagram content for a fashion brand.",
            "complexity": "Beginner",
            "key_concepts": ["content strategy", "social media", "Instagram", "engagement hooks"]
        },
        4: {
            "topic": "SEO & Search Fundamentals",
            "objective": "Learn discoverability and search intent. Reality Task: Audit a website and optimize page titles, meta descriptions, and keywords.",
            "complexity": "Intermediate",
            "key_concepts": ["SEO", "search intent", "meta descriptions", "keyword optimization"]
        },
        5: {
            "topic": "Intro to Paid Advertising",
            "objective": "Understand ad platforms, objectives, and targeting. Reality Task: Set up a simulated Meta Ads campaign with the correct campaign objective.",
            "complexity": "Intermediate",
            "key_concepts": ["Meta Ads", "paid media", "campaign objectives", "targeting"]
        },
        6: {
            "topic": "Google Ads & PPC",
            "objective": "Learn search ads, keyword intent, and optimization. Reality Task: Launch a simulated Google Ads campaign. Improve CTR above benchmark.",
            "complexity": "Intermediate",
            "key_concepts": ["Google Ads", "PPC", "CTR", "keyword intent"]
        },
        7: {
            "topic": "Ad Creatives & Landing Pages",
            "objective": "Learn conversion-focused marketing assets. Reality Task: Design banner ads and improve a landing page CTA section.",
            "complexity": "Intermediate",
            "key_concepts": ["ad creatives", "landing pages", "conversion rate optimization", "CTA"]
        },
        8: {
            "topic": "Email & Mobile Marketing",
            "objective": "Learn lifecycle marketing and retention systems. Reality Task: Write a 5-email onboarding sequence and push notification strategy.",
            "complexity": "Intermediate",
            "key_concepts": ["email marketing", "lifecycle marketing", "retention", "push notifications"]
        },
        9: {
            "topic": "Marketing Analytics & Tracking",
            "objective": "Learn data interpretation and campaign measurement. Reality Task: Analyze a GA4 report and identify why sales dropped despite traffic growth.",
            "complexity": "Advanced",
            "key_concepts": ["GA4", "marketing analytics", "data interpretation", "campaign tracking"]
        },
        10: {
            "topic": "Digital Strategy & Media Planning",
            "objective": "Combine channels into a growth system. Reality Task: Build a 6-month digital marketing strategy for a real estate brand.",
            "complexity": "Advanced",
            "key_concepts": ["digital strategy", "media planning", "channel integration", "growth systems"]
        },
        11: {
            "topic": "Campaign Optimization + Portfolio Building",
            "objective": "Learn optimization thinking and showcase work professionally. Reality Task: Optimize underperforming campaigns and prepare a client-ready portfolio.",
            "complexity": "Advanced",
            "key_concepts": ["campaign optimization", "portfolio building", "professional presentation"]
        },
        12: {
            "topic": "Boardroom Defense & Crisis Simulation",
            "objective": "Defend decisions under pressure like a real marketer. Reality Task: Present campaign results to Sola and defend your ROAS projections during a crisis scenario.",
            "complexity": "Expert",
            "key_concepts": ["boardroom defense", "crisis management", "ROAS", "executive presentation"]
        }
    },

    # ================================
    # 3B. Data Analytics Matrix
    # ================================
    "data_analytics": {
        1: {
            "topic": "Intro to Data Analytics + Excel Basics",
            "objective": "Understand what data analysts do. Learn spreadsheets confidently. Reality Task: Organize messy student records using sorting, filters, and formatting.",
            "complexity": "Beginner",
            "key_concepts": ["Excel basics", "data sorting", "filtering", "formatting"]
        },
        2: {
            "topic": "Excel Functions & Data Cleaning",
            "objective": "Learn formulas gradually. Remove fear of Excel. Reality Task: Clean duplicate customer data using IF, SUMIF, COUNTIF, TEXT functions.",
            "complexity": "Beginner",
            "key_concepts": ["Excel formulas", "data cleaning", "IF statements", "COUNTIF"]
        },
        3: {
            "topic": "Data Visualization in Excel",
            "objective": "Learn charts and storytelling basics. Reality Task: Build a simple sales dashboard for a small business owner.",
            "complexity": "Beginner",
            "key_concepts": ["Excel visualization", "dashboards", "data storytelling", "charts"]
        },
        4: {
            "topic": "Excel Mini Project",
            "objective": "Apply everything learned so far. Reality Task: Analyze a retail sales dataset and present 3 business insights.",
            "complexity": "Intermediate",
            "key_concepts": ["data analysis", "business insights", "retail data", "reporting"]
        },
        5: {
            "topic": "SQL Basics",
            "objective": "Learn databases without overwhelming syntax. Reality Task: Retrieve customer orders using SELECT, WHERE, ORDER BY.",
            "complexity": "Beginner",
            "key_concepts": ["SQL fundamentals", "SELECT", "WHERE clause", "data retrieval"]
        },
        6: {
            "topic": "Filtering, Joins & Aggregation",
            "objective": "Understand how real business data connects. Reality Task: Find top-performing products using GROUP BY and JOIN.",
            "complexity": "Intermediate",
            "key_concepts": ["SQL JOINs", "GROUP BY", "data aggregation", "relational data"]
        },
        7: {
            "topic": "Business SQL Analysis",
            "objective": "Move into analyst thinking. Reality Task: Investigate declining sales for a fintech company using SQL queries.",
            "complexity": "Intermediate",
            "key_concepts": ["business analysis", "SQL investigation", "problem solving", "fintech data"]
        },
        8: {
            "topic": "Power BI Fundamentals",
            "objective": "Learn dashboards and business reporting. Reality Task: Import CSVs and create KPI cards for revenue tracking.",
            "complexity": "Advanced",
            "key_concepts": ["Power BI", "KPIs", "revenue tracking", "data import"]
        },
        9: {
            "topic": "Power BI Visualization & DAX",
            "objective": "Understand executive-level reporting. Reality Task: Build an executive dashboard showing MoM growth and regional performance.",
            "complexity": "Advanced",
            "key_concepts": ["DAX", "executive dashboards", "MoM growth", "Power BI visualization"]
        },
        10: {
            "topic": "Python for Data Analytics",
            "objective": "Learn Python gently using analyst use cases. Reality Task: Load CSV files with Pandas and clean missing values.",
            "complexity": "Advanced",
            "key_concepts": ["Python", "Pandas", "data cleaning", "missing values"]
        },
        11: {
            "topic": "Data Analysis & Visualization",
            "objective": "Combine Python with real analysis workflows. Reality Task: Analyze ad spend vs sales performance using Pandas and Matplotlib.",
            "complexity": "Advanced",
            "key_concepts": ["Python visualization", "Matplotlib", "correlation analysis", "Pandas"]
        },
        12: {
            "topic": "Real-World Analytics Project",
            "objective": "Simulate workplace pressure and collaboration. Reality Task: Debug a broken analytics report and defend your recommendations to Sola (Tech Lead).",
            "complexity": "Expert",
            "key_concepts": ["debugging", "executive communication", "analytics defense", "tech lead review"]
        }
    },

    # ================================
    # 3C. Cyber Security Matrix
    # ================================
    "cyber_security": {
        1: {
            "topic": "Intro to Cybersecurity & Digital Safety",
            "objective": "Understand how cyber threats affect businesses and individuals. Reality Task: Investigate how a phishing attack compromised a small business.",
            "complexity": "Beginner",
            "key_concepts": ["cyber threats", "phishing", "digital safety", "incident investigation"]
        },
        2: {
            "topic": "Linux & Command Line Basics",
            "objective": "Learn terminal confidence gradually. Reality Task: Navigate server files using basic Linux commands. No GUI allowed.",
            "complexity": "Beginner",
            "key_concepts": ["Linux CLI", "file navigation", "terminal commands", "no GUI"]
        },
        3: {
            "topic": "Networking Fundamentals",
            "objective": "Understand how systems communicate. Reality Task: Trace suspicious network activity between devices.",
            "complexity": "Beginner",
            "key_concepts": ["networking basics", "network tracing", "suspicious activity", "system communication"]
        },
        4: {
            "topic": "Security Fundamentals",
            "objective": "Learn permissions, authentication, and access control. Reality Task: Audit employee permissions and remove risky access levels.",
            "complexity": "Intermediate",
            "key_concepts": ["IAM", "access control", "permissions audit", "authentication"]
        },
        5: {
            "topic": "Network Security & Firewalls",
            "objective": "Learn traffic filtering and secure configurations. Reality Task: Configure firewall rules to block insecure traffic.",
            "complexity": "Intermediate",
            "key_concepts": ["firewalls", "traffic filtering", "secure configuration", "network security"]
        },
        6: {
            "topic": "Threats, Attacks & Vulnerabilities",
            "objective": "Understand common attack methods and detection. Reality Task: Analyze logs to identify brute-force vs DDoS activity.",
            "complexity": "Intermediate",
            "key_concepts": ["log analysis", "DDoS", "brute-force", "threat detection"]
        },
        7: {
            "topic": "Authentication & Identity Protection",
            "objective": "Learn MFA, password security, and identity systems. Reality Task: Implement MFA rules and identify bypass vulnerabilities.",
            "complexity": "Advanced",
            "key_concepts": ["MFA", "identity protection", "bypass vulnerabilities", "authentication rules"]
        },
        8: {
            "topic": "Encryption & Data Security",
            "objective": "Understand cryptography and secure storage. Reality Task: Encrypt confidential files and verify integrity using hashing.",
            "complexity": "Advanced",
            "key_concepts": ["encryption", "cryptography", "hashing", "data integrity"]
        },
        9: {
            "topic": "Monitoring, Auditing & Incident Response",
            "objective": "Learn operational security workflows. Reality Task: Run vulnerability scans and prepare a risk report for management.",
            "complexity": "Advanced",
            "key_concepts": ["vulnerability scanning", "risk reporting", "auditing", "incident response"]
        },
        10: {
            "topic": "Disaster Recovery & Ransomware Response",
            "objective": "Learn business continuity under pressure. Reality Task: Respond to a ransomware attack. Isolate infected systems and restore backup operations.",
            "complexity": "Advanced",
            "key_concepts": ["disaster recovery", "ransomware", "system isolation", "business continuity"]
        },
        11: {
            "topic": "Security Documentation & Reporting",
            "objective": "Learn professional communication and reporting. Reality Task: Compile vulnerability findings into a professional security portfolio.",
            "complexity": "Advanced",
            "key_concepts": ["security reporting", "documentation", "portfolio building", "professional communication"]
        },
        12: {
            "topic": "Boardroom Defense & Security Strategy",
            "objective": "Defend technical decisions to leadership. Reality Task: Present a cybersecurity risk mitigation strategy to Sola and justify patch priorities.",
            "complexity": "Expert",
            "key_concepts": ["boardroom defense", "risk mitigation", "patch management", "security strategy"]
        }
    }
}

def get_curriculum_step(track: str, task_number: int):
    """Retrieve the specific curriculum step for a given track and task number."""
    track_key = track.lower().replace(" ", "_")
    track_curriculum = CURRICULUM.get(track_key, {})

    print("found in track curriculum: -->", track_curriculum.get(task_number))
    return track_curriculum.get(task_number)