"""
WDC Labs Curriculum Definitions.
Expanded for the 5-Day + Reality Task E-Learning Framework.
Maps specific task numbers in a track to daily learning modules, weekend reality tasks, and gamification badges.
"""
import datetime
from dateutil import parser

FRAMEWORK_DEFINITIONS = {
    "3i_principles": "Initiate, Iterate, Integrate"
}

# ============================================================
# 24-WEEK GAMIFIED PROGRESSION IDENTITY ENGINE
# ============================================================

def get_identity_for_week(track: str, week: int) -> str:
    """Dynamically maps the user's week to their gamified job title."""
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
# MASTER 24-WEEK CURRICULUM & BADGE MAPPING (FULLY EXPANDED)
# ============================================================

CURRICULUM = {
    # ================================
    # DIGITAL MARKETING MATRIX
    # ================================
    "digital_marketing": {
        1: {
            "topic": "Intro to Digital Marketing", 
            "objective": "Understand the digital marketing ecosystem and how businesses grow online.",
            "day_1": "The Digital Ecosystem: Owned Paid and Earned Media channels.",
            "day_2": "Business Growth Models: B2B vs B2C eCommerce SaaS and Local Business models.",
            "day_3": "Key Digital Metrics: Impressions Clicks CTR Conversions CAC LTV.",
            "day_4": "Competitor Research: Auditing competitors' digital presence and channels.",
            "day_5": "Marketing Audit Setup: Structuring a local business evaluation framework.",
            "reality_task": "Analyze how a local business attracts customers online. Identify strengths and weaknesses.",
            "complexity": "Beginner", "key_concepts": ["ecosystem", "business growth"], "badge_opportunity": None
        },
        2: {
            "topic": "Customer Journey & Psychology", 
            "objective": "Learn buyer behavior personas funnels and the 3i Principles.",
            "day_1": "Consumer Psychology: Triggers pain points and decision drivers.",
            "day_2": "The Marketing Funnel: TOFU (Awareness) MOFU (Consideration) BOFU (Decision).",
            "day_3": "The 3i Principles: Initiate Iterate Integrate framework.",
            "day_4": "Buyer Personas: Creating detailed customer profiles with demographics & psychographics.",
            "day_5": "Touchpoint Mapping: Mapping customer steps from discovery to purchase.",
            "reality_task": "Map the customer journey for a fintech app using the 3i Principles.",
            "complexity": "Beginner", "key_concepts": ["buyer behavior", "funnels", "3i Principles"], "badge_opportunity": "Audience Analyst"
        },
        3: {
            "topic": "Content & Social Media Basics", 
            "objective": "Learn content strategy hooks engagement and platform behavior.",
            "day_1": "Platform Mechanics: Instagram TikTok LinkedIn Twitter/X algorithms.",
            "day_2": "Hook Writing: Hook Value CTA (Call-To-Action) framework.",
            "day_3": "Content Pillars: Educational Entertaining Inspirational Promotional content.",
            "day_4": "Content Scheduling: Visual grids batching and scheduling tools.",
            "day_5": "Community Engagement: Tactics for comment management and community growth.",
            "reality_task": "Create a 1-week Instagram content plan for a fashion brand.",
            "complexity": "Beginner", "key_concepts": ["content strategy", "engagement"], "badge_opportunity": "Content Operator"
        },
        4: {
            "topic": "SEO & Search Fundamentals", 
            "objective": "Understand search intent discoverability and on-page SEO.",
            "day_1": "How Search Engines Work: Crawling Indexing and Ranking basics.",
            "day_2": "Keyword Research: Intent (Informational Navigational Transactional) & volume.",
            "day_3": "On-Page SEO 1: Title tags Meta descriptions Header tags (H1 H2).",
            "day_4": "On-Page SEO 2: Image alt text internal linking and URL structures.",
            "day_5": "SEO Audit Tools: Using basic tools (Google Search Console Ubersuggest).",
            "reality_task": "Audit a website and optimize titles meta descriptions and keywords.",
            "complexity": "Intermediate", "key_concepts": ["SEO", "search intent"], "badge_opportunity": "SEO Explorer"
        },
        5: {
            "topic": "Meta Ads Fundamentals", 
            "objective": "Learn campaign objectives audience targeting and ad structures.",
            "day_1": "Meta Business Suite Setup: Business Manager Ad Accounts and Permissions.",
            "day_2": "Campaign Hierarchy: Campaign Level (Objectives) -> Ad Set -> Ad Level.",
            "day_3": "Audience Targeting: Core Audiences Custom Audiences Lookalikes.",
            "day_4": "Budgeting & Scheduling: Daily vs Lifetime budgets bidding objectives.",
            "day_5": "Ad Setup: Formatting Single Image Carousel and Video ads.",
            "reality_task": "Set up a simulated Meta Ads campaign for lead generation.",
            "complexity": "Intermediate", "key_concepts": ["Meta Ads", "targeting"], "badge_opportunity": None
        },
        6: {
            "topic": "Google Ads & PPC", 
            "objective": "Learn search advertising keyword intent and bidding strategies.",
            "day_1": "Intro to PPC & Google Search Ads: Auction mechanics & Quality Score.",
            "day_2": "Match Types: Broad Match Phrase Match Exact Match and Negative Keywords.",
            "day_3": "Ad Copywriting: Headlines Descriptions and Responsive Search Ads (RSA).",
            "day_4": "Ad Extensions (Assets): Sitelinks Callouts Structured Snippets.",
            "day_5": "Bidding Strategies: Manual CPC Maximize Clicks Target CPA.",
            "reality_task": "Launch a Google Ads campaign. Improve CTR above benchmark.",
            "complexity": "Intermediate", "key_concepts": ["Google Ads", "PPC", "bidding"], "badge_opportunity": "Paid Media Operator"
        },
        7: {
            "topic": "Creatives & Landing Pages", 
            "objective": "Learn conversion-focused copywriting visuals and CTAs.",
            "day_1": "Direct Response Copywriting: AIDA (Attention Interest Desire Action) framework.",
            "day_2": "Visual Design Principles: Contrast Hierarchy and Ad Visual Testing.",
            "day_3": "Landing Page Essentials: Above-the-fold layout value prop social proof.",
            "day_4": "Call to Actions (CTAs): High-converting copy and button placements.",
            "day_5": "Landing Page Wireframing: Designing high-converting mockups.",
            "reality_task": "Improve a poor-performing landing page and redesign ad creatives.",
            "complexity": "Intermediate", "key_concepts": ["copywriting", "landing pages"], "badge_opportunity": None
        },
        8: {
            "topic": "Email & Mobile Marketing", 
            "objective": "Learn lifecycle marketing and customer retention systems.",
            "day_1": "Lifecycle Marketing: Lead Nurturing Post-purchase Win-back flows.",
            "day_2": "Email Copywriting: Subject line hook body copy preview text optimization.",
            "day_3": "Onboarding Sequences: Writing multi-day welcome email campaigns.",
            "day_4": "Mobile Marketing: SMS and Push Notification timing & best practices.",
            "day_5": "Email Deliverability: Spam triggers list hygiene open rates CTR.",
            "reality_task": "Write a 5-email onboarding flow and mobile push strategy.",
            "complexity": "Intermediate", "key_concepts": ["email marketing", "retention"], "badge_opportunity": None
        },
        9: {
            "topic": "Analytics & Tracking", 
            "objective": "Learn attribution KPIs GA4 Meta Pixel and tracking systems.",
            "day_1": "Web Analytics Intro: Tracking code mechanics and GA4 overview.",
            "day_2": "Pixel & Conversion Setup: Meta Pixel Google Tag Manager event setup.",
            "day_3": "UTM Parameters: Tagging URLs correctly for source/medium tracking.",
            "day_4": "Attribution Models: First Click Last Click Linear Data-driven attribution.",
            "day_5": "Diagnostic Analytics: Diagnosing traffic drops and conversion leaks in GA4.",
            "reality_task": "Traffic increased but sales dropped. Analyze the GA4 report and identify the issue.",
            "complexity": "Advanced", "key_concepts": ["GA4", "Meta Pixel", "attribution"], "badge_opportunity": None
        },
        10: {
            "topic": "Media Planning & Strategy", 
            "objective": "Learn budgeting KPI planning and channel allocation.",
            "day_1": "Budget Allocation: Dividing spend across TOFU MOFU BOFU.",
            "day_2": "Forecasting KPIs: Estimating traffic leads and revenue based on benchmark metrics.",
            "day_3": "Channel Mix Strategy: Choosing between Social Search Email and Display.",
            "day_4": "Campaign Timelines: GANTT charts for campaign execution & asset deadlines.",
            "day_5": "Media Plan Assembly: Structuring a complete 6-month budget strategy.",
            "reality_task": "Create a 6-month media plan for a real estate company.",
            "complexity": "Advanced", "key_concepts": ["budgeting", "media planning"], "badge_opportunity": None
        },
        11: {
            "topic": "Campaign Optimization", 
            "objective": "Learn testing scaling creative fatigue and ROAS improvement.",
            "day_1": "Performance Auditing: Identifying underperforming ads and fatigue.",
            "day_2": "A/B Testing Framework: Hypothesis building variable isolation sample sizes.",
            "day_3": "Fixing ROAS: Reducing CAC through ad refresh and targeting adjustments.",
            "day_4": "Bidding Adjustments: Scaling winning ad sets trimming poor performers.",
            "day_5": "Emergency Rescue Tactics: Quick tweaks to save failing campaigns.",
            "reality_task": "Fix underperforming campaigns before Tolu cuts the budget.",
            "complexity": "Advanced", "key_concepts": ["ROAS", "scaling", "optimization"], "badge_opportunity": "Optimization Expert"
        },
        12: {
            "topic": "Portfolio + Boardroom Defense", 
            "objective": "Learn reporting presentation and client communication skills.",
            "day_1": "Portfolio Structuring: Showcasing campaigns ad copy and ROI metrics.",
            "day_2": "Reporting Frameworks: Designing client/executive performance dashboards.",
            "day_3": "Case Study Writing: Problem Strategy Execution Results format.",
            "day_4": "Objections & Defense: Preparing answers for ROI and budget inquiries.",
            "day_5": "Mock Pitch: Presenting campaign strategy under presentation conditions.",
            "reality_task": "Present campaign results to Sola and defend your ROAS projections.",
            "complexity": "Expert", "key_concepts": ["reporting", "client communication"], "badge_opportunity": None
        },
        13: {
            "topic": "Advanced Meta Ads", 
            "objective": "Learn retargeting CBO lookalikes and scaling systems.",
            "day_1": "Campaign Budget Optimization (CBO) vs ABO scaling strategies.",
            "day_2": "High-Budget Scaling: Horizontal scaling (audiences) vs Vertical scaling (budget).",
            "day_3": "Advanced Retargeting: Time-window retargeting (3-day 7-day 30-day).",
            "day_4": "Dynamic Product Ads (DPA): Setting up catalog sales for e-commerce.",
            "day_5": "Creative Fatigue System: Building a creative pipeline to combat ad burnout.",
            "reality_task": "Scale a winning campaign from ₦50k to ₦500k budget without killing ROAS.",
            "complexity": "Expert", "key_concepts": ["CBO", "lookalikes", "retargeting"], "badge_opportunity": None
        },
        14: {
            "topic": "Advanced Google Ads", 
            "objective": "Learn PMAX YouTube Ads Display Ads and advanced optimization.",
            "day_1": "Performance Max (PMAX) Campaigns: Asset groups and signal targeting.",
            "day_2": "YouTube Ads: Skippable vs non-skippable formats hook strategy.",
            "day_3": "Display & Remarketing: Google Display Network targeting and placement exclusions.",
            "day_4": "Search Term Cleanups: Search terms report auditing and negative match lists.",
            "day_5": "Smart Bidding: Target ROAS (tROAS) and Target CPA (tCPA) optimization.",
            "reality_task": "Fix a Google Ads account wasting spend on low-intent traffic.",
            "complexity": "Expert", "key_concepts": ["PMAX", "YouTube Ads"], "badge_opportunity": None
        },
        15: {
            "topic": "Conversion Rate Optimization (CRO)", 
            "objective": "Learn heatmaps A/B testing and user behavior optimization.",
            "day_1": "Heatmap Analysis: Analyzing Hotjar / Clarity clicks scrolls and rage clicks.",
            "day_2": "User Friction Audits: Identifying form drop-offs page load friction and UX bugs.",
            "day_3": "Copy & Value Proposition Testing: Testing headline changes for conversion lifts.",
            "day_4": "Checkout Optimization: Reducing cart abandonment steps.",
            "day_5": "A/B Test Execution: Setting up Google Optimize / VWO experiments.",
            "reality_task": "Increase landing page conversion rate from 1.2% to 3%.",
            "complexity": "Expert", "key_concepts": ["CRO", "A/B testing"], "badge_opportunity": None
        },
        16: {
            "topic": "Full Funnel Systems", 
            "objective": "Learn multi-touch attribution and acquisition-to-retention systems.",
            "day_1": "Multi-Touch Funnels: Connecting top-of-funnel ads to retention sequences.",
            "day_2": "Cross-Channel Synchronization: Coordinating Meta Google and Email messaging.",
            "day_3": "Offer Architecture: Tripwires lead magnets order bumps upsells.",
            "day_4": "Measurement Architecture: Tracking user progression from click to repeat buyer.",
            "day_5": "Funnel Mapping: Visualizing full funnel maps in Whimsical / Funnelytics.",
            "reality_task": "Build a complete acquisition + retargeting funnel for an ecommerce brand.",
            "complexity": "Expert", "key_concepts": ["multi-touch attribution", "funnels"], "badge_opportunity": "Funnel Builder"
        },
        17: {
            "topic": "Advanced Analytics", 
            "objective": "Learn attribution models cohorts CAC and customer LTV.",
            "day_1": "Cohort Analysis: Retention rates and revenue per cohort over time.",
            "day_2": "CAC & LTV Economics: LTV:CAC ratios payback period calculation.",
            "day_3": "Multi-Touch Attribution: W-shaped Time-Decay First/Last touch comparison.",
            "day_4": "Unit Economics Debugging: Diagnosing rising CAC in competitive auctions.",
            "day_5": "Strategic Analytics Reporting: Data-backed growth recommendations.",
            "reality_task": "Identify why CAC increased despite higher conversion rates.",
            "complexity": "Expert", "key_concepts": ["CAC", "LTV", "cohorts"], "badge_opportunity": "Analytics Specialist"
        },
        18: {
            "topic": "Marketing Automation", 
            "objective": "Learn CRM workflows automation systems and lead nurturing.",
            "day_1": "CRM Architectures: HubSpot / ActiveCampaign lead status setups.",
            "day_2": "Lead Scoring: Points-based systems for intent (page views email clicks).",
            "day_3": "Automated Workflows: If/Then logic branching for B2B nurture tracks.",
            "day_4": "Webhook Integrations: Connecting forms CRMs and ad platforms via Zapier/Make.",
            "day_5": "Automation Testing: Debugging broken automation steps and triggers.",
            "reality_task": "Build an automated lead nurturing workflow for a B2B company.",
            "complexity": "Expert", "key_concepts": ["CRM", "lead nurturing"], "badge_opportunity": None
        },
        19: {
            "topic": "Growth Marketing Systems", 
            "objective": "Learn experimentation frameworks and Pirate Metrics.",
            "day_1": "Pirate Metrics (AARRR): Acquisition Activation Retention Referral Revenue.",
            "day_2": "Experimentation Frameworks: ICE (Impact Confidence Ease) scoring.",
            "day_3": "Activation Rate Optimization: Improving early user onboarding success.",
            "day_4": "Viral Loops & Referral Systems: Designing user referral incentives.",
            "day_5": "Growth Sprints: Structuring 2-week growth experimentation cycles.",
            "reality_task": "Design a growth experiment to improve activation by 25%.",
            "complexity": "Expert", "key_concepts": ["Pirate Metrics", "experimentation"], "badge_opportunity": "Growth Strategist"
        },
        20: {
            "topic": "AI in Marketing", 
            "objective": "Learn AI-assisted workflows prompting and automation tools.",
            "day_1": "Generative AI for Copy: Writing ad variations using advanced prompting.",
            "day_2": "AI Visual Generation: Creating ad assets with Midjourney / Canva AI.",
            "day_3": "Audience Research with AI: Mining forums and reviews using LLMs.",
            "day_4": "Automated Reporting: Using AI plugins to analyze campaign CSV data.",
            "day_5": "AI Workflow Integration: Building end-to-end AI-assisted marketing workflows.",
            "reality_task": "Use AI tools to optimize ad copy segmentation and reporting workflows.",
            "complexity": "Expert", "key_concepts": ["AI tools", "automation"], "badge_opportunity": None
        },
        21: {
            "topic": "Crisis & Reputation Management", 
            "objective": "Learn PR response brand recovery and communication under pressure.",
            "day_1": "Social Listening Setup: Monitoring brand sentiment and trend spikes.",
            "day_2": "Crisis Classification: Categorizing threats (Low Medium Critical).",
            "day_3": "Statement Drafting: Writing transparent empathetic public responses.",
            "day_4": "De-escalation Frameworks: Managing social media backlash in real-time.",
            "day_5": "24-Hour Recovery Playbook: Post-crisis brand rebuilding strategies.",
            "reality_task": "500 angry tweets are trending. Create a 24-hour response strategy.",
            "complexity": "Expert", "key_concepts": ["PR response", "reputation management"], "badge_opportunity": "Crisis Manager"
        },
        22: {
            "topic": "Client & Stakeholder Management", 
            "objective": "Learn reporting negotiation and expectation management.",
            "day_1": "Managing Expectations: Setting realistic ROAS & KPI targets up front.",
            "day_2": "Difficult Conversations: Communicating budget overruns or poor performance.",
            "day_3": "Value-Based Upselling: Presenting growth opportunities to expand scope.",
            "day_4": "Client Reporting Meetings: Conducting effective monthly performance reviews.",
            "day_5": "SLA & Scope Defense: Preventing scope creep while keeping clients happy.",
            "reality_task": "Defend delayed campaign results to an angry client.",
            "complexity": "Expert", "key_concepts": ["negotiation", "expectation management"], "badge_opportunity": None
        },
        23: {
            "topic": "Agency Simulation", 
            "objective": "Learn collaboration prioritization and campaign operations.",
            "day_1": "Multi-Client Management: Prioritizing focus across competing accounts.",
            "day_2": "Resource Allocation: Balancing creative media spend and operational hours.",
            "day_3": "Emergency Priority Shifts: Re-allocating effort when key clients face crises.",
            "day_4": "Team Workflows: Delegating tasks between media buyers and designers.",
            "day_5": "Account Health Checks: Auditing operational risks across all campaigns.",
            "reality_task": "Manage 3 client campaigns simultaneously with changing priorities.",
            "complexity": "Expert", "key_concepts": ["campaign operations", "prioritization"], "badge_opportunity": None
        },
        24: {
            "topic": "Executive Boardroom Defense", 
            "objective": "Learn leadership communication and strategic decision-making.",
            "day_1": "12-Month Growth Roadmap: Scaling spend channels and revenue targets.",
            "day_2": "Executive Financial Modeling: Forecasting ROAS LTV and CAC at scale.",
            "day_3": "Presentation Mastery: Structuring C-suite presentations for maximum buy-in.",
            "day_4": "Live Board Defense Prep: Practicing answers to critical executive questions.",
            "day_5": "Strategy Polish: Finalizing pitch deck and portfolio documentation.",
            "reality_task": "Present a 12-month growth strategy to the executive board and defend every KPI.",
            "complexity": "Expert", "key_concepts": ["leadership", "decision-making"], "badge_opportunity": "Boardroom Certified"
        }
    },

    # ================================
    # DATA ANALYTICS MATRIX
    # ================================
    "data_analytics": {
        1: {
            "topic": "Intro to Data Analytics", "objective": "Understand what data analysts do and how businesses use data.",
            "day_1": "What is Data Analytics? Types of analytics (Descriptive Diagnostic Predictive Prescriptive).",
            "day_2": "The Data Life Cycle & Business Context: How companies use data to make decisions.",
            "day_3": "Key Metrics & KPIs: Metrics vs. Dimensions quantitative vs. qualitative data.",
            "day_4": "Data Privacy & Ethics: Handling sensitive information and basic data governance.",
            "day_5": "Dataset Exploration: Opening business sales datasets and identifying structure.",
            "reality_task": "Analyze sales records from a small business and identify basic patterns.",
            "complexity": "Beginner", "key_concepts": ["business logic", "patterns"], "badge_opportunity": None
        },
        2: {
            "topic": "Excel Basics", "objective": "Learn spreadsheets formatting sorting and filtering confidently.",
            "day_1": "Interface & Navigation: Workbook layout shortcuts and basic formatting.",
            "day_2": "Data Entry & Cleanup: Removing duplicates blank rows and fixing data types.",
            "day_3": "Sorting & Multi-level Filtering: Organizing datasets logically.",
            "day_4": "Absolute & Relative Cell Referencing ($ sign usage).",
            "day_5": "Data Validation: Restricting input fields and creating dropdown lists.",
            "reality_task": "Clean messy employee records using filters and formatting tools.",
            "complexity": "Beginner", "key_concepts": ["Excel", "filtering", "formatting"], "badge_opportunity": "Spreadsheet Survivor"
        },
        3: {
            "topic": "Excel Functions & Formulas", "objective": "Learn formulas and data cleaning workflows.",
            "day_1": "Basic Aggregations: SUM AVERAGE MIN MAX COUNT COUNTA.",
            "day_2": "Text Functions: LEFT RIGHT MID CONCATENATE TRIM UPPER LOWER.",
            "day_3": "Logical Functions: Single IF statements and nested IF logic.",
            "day_4": "Conditional Sums: SUMIF SUMIFS COUNTIF COUNTIFS.",
            "day_5": "Lookup Functions: VLOOKUP XLOOKUP and handling #N/A errors.",
            "reality_task": "Fix inconsistent customer data using IF SUMIF COUNTIF and TEXT functions.",
            "complexity": "Beginner", "key_concepts": ["IF", "SUMIF", "COUNTIF"], "badge_opportunity": "Formula Operator"
        },
        4: {
            "topic": "Data Visualization in Excel", "objective": "Learn charts dashboards and storytelling basics.",
            "day_1": "Chart Principles: Choosing the right chart (Bar Line Pie Scatter).",
            "day_2": "Chart Formatting: Labels titles legends and color palettes for business.",
            "day_3": "Pivot Tables Basics: Creating summary tables from raw data.",
            "day_4": "Pivot Charts & Slicers: Interactive filtering for executive views.",
            "day_5": "Dashboard Layout: Designing a clean 1-page Excel dashboard layout.",
            "reality_task": "Create a simple sales dashboard for a business owner.",
            "complexity": "Beginner", "key_concepts": ["dashboards", "charts"], "badge_opportunity": None
        },
        5: {
            "topic": "Power Query & Data Cleaning", "objective": "Learn transformation and structured cleaning workflows.",
            "day_1": "Introduction to Power Query: ETL process (Extract Transform Load).",
            "day_2": "Connecting Data: Importing CSV Excel and Web data into Power Query.",
            "day_3": "Transformations: Splitting columns unpivoting merging text and replacing values.",
            "day_4": "Merging & Appending Queries: Combining multiple sheets/files into one table.",
            "day_5": "Data Types & Errors: Handling null values and type conversions.",
            "reality_task": "Import messy sales files and prepare them for reporting.",
            "complexity": "Intermediate", "key_concepts": ["Power Query", "transformation"], "badge_opportunity": None
        },
        6: {
            "topic": "Excel Business Project", "objective": "Apply Excel knowledge to solve business problems.",
            "day_1": "Project Scoping: Understanding business requirements and data schemas.",
            "day_2": "Data Cleaning & Audit: Applying Power Query to clean retail datasets.",
            "day_3": "Data Analysis: Calculating MoM growth top products and customer categories.",
            "day_4": "Dashboard Build: Assembling visual reporting layouts in Excel.",
            "day_5": "Insight Generation: Writing clear executive summaries based on findings.",
            "reality_task": "Analyze retail data and present 3 business recommendations.",
            "complexity": "Intermediate", "key_concepts": ["business recommendations", "retail data"], "badge_opportunity": "Insight Hunter"
        },
        7: {
            "topic": "SQL Basics", "objective": "Learn databases SELECT statements filtering and sorting.",
            "day_1": "Introduction to Relational Databases (RDBMS) & SQL Syntax.",
            "day_2": "Data Retrieval: SELECT DISTINCT and column aliasing (AS).",
            "day_3": "Filtering Data: WHERE clause operators (= > < LIKE IN BETWEEN).",
            "day_4": "Sorting Results: ORDER BY (ASC/DESC) and limiting outputs (LIMIT/TOP).",
            "day_5": "SQL Practice: Writing queries against multi-table business databases.",
            "reality_task": "Retrieve customer orders using SQL queries.",
            "complexity": "Intermediate", "key_concepts": ["SQL", "SELECT", "filtering"], "badge_opportunity": "SQL Investigator"
        },
        8: {
            "topic": "SQL Joins & Aggregation", "objective": "Learn joins grouping and business analysis queries.",
            "day_1": "Aggregation Functions: COUNT SUM AVG MIN MAX.",
            "day_2": "Grouping Data: GROUP BY and filtering aggregates with HAVING.",
            "day_3": "SQL Joins 1: INNER JOIN vs LEFT JOIN explained with ERD diagrams.",
            "day_4": "SQL Joins 2: RIGHT JOIN and FULL OUTER JOIN edge cases.",
            "day_5": "Multi-Table Joins: Connecting 3+ tables to answer complex business questions.",
            "reality_task": "Find top-performing products using JOIN and GROUP BY.",
            "complexity": "Intermediate", "key_concepts": ["JOIN", "GROUP BY"], "badge_opportunity": None
        },
        9: {
            "topic": "Intermediate SQL Analysis", "objective": "Learn analytical SQL workflows.",
            "day_1": "Subqueries: Scalar vs multi-row subqueries in WHERE and FROM.",
            "day_2": "Common Table Expressions (CTEs): Writing clean readable WITH clauses.",
            "day_3": "String & Date Functions: DATE_TRUNC EXTRACT CONCAT SUBSTRING.",
            "day_4": "Conditional Logic in SQL: CASE WHEN ... THEN ... ELSE ... END.",
            "day_5": "Performance Optimization: Basic indexing concepts and query efficiency.",
            "reality_task": "Investigate declining sales trends using SQL queries.",
            "complexity": "Advanced", "key_concepts": ["sales trends", "SQL workflows"], "badge_opportunity": None
        },
        10: {
            "topic": "Power BI Fundamentals", "objective": "Learn dashboarding and business intelligence basics.",
            "day_1": "Intro to Power BI Desktop: Interface Data view Model view Report view.",
            "day_2": "Data Ingestion: Connecting Power BI to SQL Databases and Excel files.",
            "day_3": "Star Schema Data Modeling: Fact tables vs Dimension tables.",
            "day_4": "Basic Visuals: Cards Bar Charts Line Charts and Slicers.",
            "day_5": "Visual Interactivity: Configuring interactions drill-downs and cross-filtering.",
            "reality_task": "Build KPI cards for revenue and sales performance.",
            "complexity": "Advanced", "key_concepts": ["Power BI", "KPI cards"], "badge_opportunity": "Dashboard Specialist"
        },
        11: {
            "topic": "Power BI Dashboards & DAX", "objective": "Learn advanced dashboards and executive reporting.",
            "day_1": "Intro to DAX (Data Analysis Expressions): Calculated Columns vs Measures.",
            "day_2": "Essential DAX Functions: SUM AVERAGE COUNTROWS DISTINCTCOUNT.",
            "day_3": "The CALCULATE Function: Modifying filter context in Power BI.",
            "day_4": "Time Intelligence in DAX: DATEADD SAMEPERIODLASTYEAR YTD.",
            "day_5": "Executive Dashboard Formatting: Theme colors alignment and navigation UX.",
            "reality_task": "Create an executive dashboard showing MoM growth trends.",
            "complexity": "Advanced", "key_concepts": ["DAX", "executive reporting"], "badge_opportunity": None
        },
        12: {
            "topic": "Portfolio + Analyst Defense", "objective": "Learn reporting and stakeholder communication.",
            "day_1": "Portfolio Setup: Structuring GitHub / Notion project documentation.",
            "day_2": "Executive Summaries: Writing business-oriented insights not technical jargon.",
            "day_3": "Presentation Deck Creation: Designing clear impactful slides.",
            "day_4": "Q&A Prep: Anticipating stakeholder questions and pushback on metrics.",
            "day_5": "Final Rehearsal: Pitching findings within a strict time limit.",
            "reality_task": "Present business insights to Sola and defend your recommendations.",
            "complexity": "Expert", "key_concepts": ["stakeholder defense", "insights"], "badge_opportunity": None
        },
        13: {
            "topic": "Python for Data Analytics", "objective": "Learn Python fundamentals using business datasets.",
            "day_1": "Intro to Python & Jupyter Notebooks: Variables data types and syntax.",
            "day_2": "Python Control Structures: Lists Dictionaries If/Else and For loops.",
            "day_3": "Intro to Pandas: Series vs DataFrames.",
            "day_4": "Loading Datasets: Reading CSV Excel and JSON files into Pandas.",
            "day_5": "Data Inspection: .head() .info() .describe() and checking missing values.",
            "reality_task": "Load and clean CSV files using Pandas.",
            "complexity": "Expert", "key_concepts": ["Python", "Pandas", "CSV"], "badge_opportunity": None
        },
        14: {
            "topic": "Data Manipulation with Pandas", "objective": "Learn filtering grouping merging and transformations.",
            "day_1": "Filtering Data: Boolean indexing and conditional queries in Pandas.",
            "day_2": "Data Cleaning: .fillna() .dropna() .astype() .replace().",
            "day_3": "Aggregations: .groupby() and .agg() methods for multi-level metrics.",
            "day_4": "Merging Data: pd.merge() and pd.concat() (Joins in Python).",
            "day_5": "Feature Engineering: Creating calculated columns and applying lambda functions.",
            "reality_task": "Analyze regional sales performance using Pandas.",
            "complexity": "Expert", "key_concepts": ["Pandas", "data manipulation"], "badge_opportunity": None
        },
        15: {
            "topic": "Python Visualization", "objective": "Learn Matplotlib and Seaborn for storytelling.",
            "day_1": "Intro to Matplotlib: Line plots scatter plots and figure layouts.",
            "day_2": "Intro to Seaborn: Categorical plots bar charts and heatmaps.",
            "day_3": "Customizing Visuals: Color palettes titles labels and plot styling.",
            "day_4": "Visualizing Distributions: Histograms Box plots and KDE curves.",
            "day_5": "Multi-plot Grids: Creating subplot grids for comparative analysis.",
            "reality_task": "Visualize ad spend vs sales performance trends.",
            "complexity": "Expert", "key_concepts": ["Matplotlib", "Seaborn"], "badge_opportunity": None
        },
        16: {
            "topic": "Working with Big Data Files", "objective": "Learn efficient workflows for large datasets.",
            "day_1": "Memory Management: Python memory footprint and chunk processing concepts.",
            "day_2": "Optimized File Formats: Reading Parquet & Feather vs CSV files.",
            "day_3": "Vectorization: Replacing slow Python loops with optimized NumPy/Pandas logic.",
            "day_4": "Large Dataset Filtering: Low-memory column selection and data type downcasting.",
            "day_5": "Out-of-Memory Workflows: Intro to Polars / Dask for multi-GB data.",
            "reality_task": "Analyze a 2GB transaction file without crashing the system.",
            "complexity": "Expert", "key_concepts": ["big data", "efficiency"], "badge_opportunity": None
        },
        17: {
            "topic": "Statistical Analysis", "objective": "Learn averages variance correlations and forecasting basics.",
            "day_1": "Central Tendency & Dispersion: Mean Median Variance Standard Deviation.",
            "day_2": "Probability Distributions: Normal distribution Z-scores and percentiles.",
            "day_3": "Correlation vs Causation: Pearson correlation matrix and heatmaps.",
            "day_4": "Hypothesis Testing: Intro to p-values A/B testing logic and T-tests.",
            "day_5": "Churn Analysis Drivers: Evaluating features influencing customer retention.",
            "reality_task": "Identify the strongest factor influencing customer churn.",
            "complexity": "Expert", "key_concepts": ["variance", "correlations", "forecasting"], "badge_opportunity": None
        },
        18: {
            "topic": "Advanced Power BI & DAX", "objective": "Learn advanced reporting logic and automation.",
            "day_1": "Dynamic Parameters: Field parameters and dynamic measures.",
            "day_2": "Advanced DAX: RANKX EARLIER and complex filter modifications.",
            "day_3": "Row-Level Security (RLS): Restricting data access based on user role.",
            "day_4": "Performance Analyzer: Optimizing slow Power BI queries and DAX code.",
            "day_5": "Dashboard UX/UI: Tooltips bookmarks and mobile layout view.",
            "reality_task": "Build a dynamic executive dashboard with drill-down analysis.",
            "complexity": "Expert", "key_concepts": ["DAX", "drill-down analysis"], "badge_opportunity": None
        },
        19: {
            "topic": "Business Reporting & Communication", "objective": "Learn insight presentation and stakeholder reporting.",
            "day_1": "Storytelling Frameworks: Context Conflict Resolution in data presentation.",
            "day_2": "Eliminating Noise: De-cluttering reports and highlighting key insights.",
            "day_3": "Writing for C-Suite: Translating technical metrics into financial ROI.",
            "day_4": "Slide Deck Design: Executive dashboard slide templates.",
            "day_5": "Presenting Uncertainties: Communicating margins of error and assumptions.",
            "reality_task": "Turn technical findings into a boardroom-ready report.",
            "complexity": "Expert", "key_concepts": ["boardroom reporting", "communication"], "badge_opportunity": "Data Storyteller"
        },
        20: {
            "topic": "Analytics Automation", "objective": "Learn scheduled reporting and automated workflows.",
            "day_1": "Automation Architecture: Scheduled tasks and batch data workflows.",
            "day_2": "Python Scripting: Auto-executing data cleaning and generation scripts.",
            "day_3": "Power BI Gateway: Setting up automated dataset scheduled refreshes.",
            "day_4": "Email Alerts: Triggering automated notification emails when metrics cross thresholds.",
            "day_5": "Workflow Debugging: Error logging and handling failed automation scripts.",
            "reality_task": "Automate weekly reporting for a marketing team.",
            "complexity": "Expert", "key_concepts": ["automation", "scheduled reporting"], "badge_opportunity": "Automation Specialist"
        },
        21: {
            "topic": "Predictive Analytics Foundations", "objective": "Learn trend forecasting and predictive thinking.",
            "day_1": "Time Series Basics: Trend Seasonality and Cyclical patterns.",
            "day_2": "Moving Averages: Simple & Exponential Moving Averages for forecasting.",
            "day_3": "Linear Regression Intro: Simple linear models in Excel / Python.",
            "day_4": "Evaluating Forecasts: Mean Absolute Error (MAE) and accuracy rates.",
            "day_5": "Scenario Analysis: Best-case worst-case and expected revenue scenarios.",
            "reality_task": "Predict next quarter’s sales performance using historical data.",
            "complexity": "Expert", "key_concepts": ["predictive analytics", "forecasting"], "badge_opportunity": "Predictive Analyst"
        },
        22: {
            "topic": "Cross-Department Data Analysis", "objective": "Learn collaborative business analytics workflows.",
            "day_1": "Multi-Department Metrics: Aligning Finance Sales and Marketing KPIs.",
            "day_2": "Customer Journey Mapping: Connecting ad spend to actual revenue leakage.",
            "day_3": "Data Reconciliation: Identifying discrepancy between CRM and Finance logs.",
            "day_4": "Cohort Analysis: Tracking user retention cohorts over time.",
            "day_5": "Cross-Department Dashboards: Unified operational metrics reporting.",
            "reality_task": "Analyze finance sales and marketing datasets to identify revenue leakage.",
            "complexity": "Expert", "key_concepts": ["cross-department", "revenue leakage"], "badge_opportunity": None
        },
        23: {
            "topic": "Real-World Data Crisis Simulation", "objective": "Learn debugging and operational analytics pressure handling.",
            "day_1": "Diagnostic Analytics: Investigating sudden metric drops under pressure.",
            "day_2": "Finding Broken Pipelines: Auditing broken SQL scripts and calculation errors.",
            "day_3": "Fast Data Patching: Applying hotfixes to erroneous data fields.",
            "day_4": "Stakeholder Management: Writing incident updates to senior management.",
            "day_5": "Root Cause Analysis (RCA): Creating post-mortem reports.",
            "reality_task": "Fix broken reports before the executive meeting starts.",
            "complexity": "Expert", "key_concepts": ["debugging", "crisis handling"], "badge_opportunity": "Crisis Analyst"
        },
        24: {
            "topic": "Boardroom Defense & Strategic Analytics", "objective": "Learn leadership communication and strategic insight defense.",
            "day_1": "12-Month Analytics Roadmap: Defining tools team scaling and infrastructure.",
            "day_2": "Estimating Analytics ROI: Proving financial value of data investments.",
            "day_3": "Final Executive Presentation Deck: Fine-tuning long-term recommendations.",
            "day_4": "Mock Defense: Responding to aggressive board-level questioning.",
            "day_5": "Final Polish: Finalizing portfolio and strategic documentation.",
            "reality_task": "Present a 12-month business intelligence strategy to the executive board.",
            "complexity": "Expert", "key_concepts": ["strategy", "executive leadership"], "badge_opportunity": "Executive Analyst"
        }
    },

    # ================================
    # CYBER SECURITY MATRIX
    # ================================
    "cyber_security": {
        1: {
            "topic": "Intro to Cybersecurity", "objective": "Understand cybersecurity digital threats and business risks.",
            "day_1": "Core Pillars: CIA Triad (Confidentiality Integrity Availability).",
            "day_2": "Threat Landscape: Malware Ransomware Social Engineering Insider Threats.",
            "day_3": "Threat Actors: Script Kiddies Hacktivists APTs Cybercriminals.",
            "day_4": "Attack Vectors: Phishing anatomy baiting and pretexting tactics.",
            "day_5": "Business Risk: Financial operational and reputational impact of breaches.",
            "reality_task": "Investigate how a phishing attack compromised a small business.",
            "complexity": "Beginner", "key_concepts": ["phishing", "threats", "business risk"], "badge_opportunity": None
        },
        2: {
            "topic": "Linux & Command Line Basics", "objective": "Build confidence navigating systems using CLI.",
            "day_1": "Intro to Linux OS: Filesystem hierarchy (/ /etc /var /home).",
            "day_2": "File Operations: ls cd pwd mkdir cp mv rm.",
            "day_3": "Text Processing: cat grep less head tail nano.",
            "day_4": "Permissions & Ownership: chmod (numeric/symbolic) chown sudo.",
            "day_5": "System Management: ps top df du environment variables.",
            "reality_task": "Navigate server directories using Linux commands only.",
            "complexity": "Beginner", "key_concepts": ["CLI", "directories", "permissions"], "badge_opportunity": "Linux Operator"
        },
        3: {
            "topic": "Networking Fundamentals", "objective": "Learn how systems communicate and exchange data.",
            "day_1": "Networking Models: OSI 7-Layer Model vs TCP/IP Model.",
            "day_2": "IP Addressing & Subnetting: IPv4 vs IPv6 Public vs Private IPs.",
            "day_3": "Core Protocols: TCP vs UDP DNS DHCP HTTP/HTTPS.",
            "day_4": "Network Traffic Analysis: MAC addresses ARP and routing concepts.",
            "day_5": "Network Tools: Using ping traceroute netstat/ss nslookup.",
            "reality_task": "Trace suspicious network activity between devices.",
            "complexity": "Beginner", "key_concepts": ["TCP/IP", "DNS", "packet tracing"], "badge_opportunity": None
        },
        4: {
            "topic": "Security Fundamentals", "objective": "Learn authentication permissions and access control.",
            "day_1": "Authentication vs Authorization vs Accounting (AAA Framework).",
            "day_2": "Access Control Models: DAC MAC RBAC (Role-Based Access Control).",
            "day_3": "Principle of Least Privilege & Separation of Duties.",
            "day_4": "Identity Auditing: Finding inactive accounts and over-privileged permissions.",
            "day_5": "Password Security: Hashing policies salt and password complexity enforcement.",
            "reality_task": "Audit employee permissions and remove risky access levels.",
            "complexity": "Intermediate", "key_concepts": ["IAM", "authentication", "access control"], "badge_opportunity": None
        },
        5: {
            "topic": "Firewalls & Network Security", "objective": "Learn traffic filtering and secure configurations.",
            "day_1": "Firewall Architecture: Packet Filtering vs Stateful Inspection vs Next-Gen Firewalls.",
            "day_2": "Network Segmentation: DMZs VLANs and isolation boundaries.",
            "day_3": "Firewall Rule Writing: Inbound vs Outbound rule syntax (Port IP Action).",
            "day_4": "Network Access Control Lists (NACLs) & Security Groups.",
            "day_5": "Traffic Auditing: Reviewing blocked vs allowed firewall logs.",
            "reality_task": "Configure firewall rules to block insecure traffic.",
            "complexity": "Intermediate", "key_concepts": ["firewall rules", "port filtering"], "badge_opportunity": "Network Defender"
        },
        6: {
            "topic": "Threats & Vulnerabilities", "objective": "Learn attack types and detection methods.",
            "day_1": "Attack Tactics: Brute-force attacks Password Spraying Credential Stuffing.",
            "day_2": "Denial of Service: DoS vs DDoS Amplification attacks Botnets.",
            "day_3": "Vulnerability Management: CVE system CVSS scoring and vulnerability lifecycles.",
            "day_4": "Log Analysis Basics: Parsing auth logs for repeated failure patterns.",
            "day_5": "Attack Identification: Differentiating brute-force logs from DDoS signatures.",
            "reality_task": "Analyze logs to identify brute-force vs DDoS activity.",
            "complexity": "Intermediate", "key_concepts": ["DDoS", "brute-force", "log analysis"], "badge_opportunity": "Threat Hunter"
        },
        7: {
            "topic": "Authentication & MFA", "objective": "Learn identity protection and MFA systems.",
            "day_1": "Authentication Factors: Something you know have are somewhere you are.",
            "day_2": "Multi-Factor Authentication (MFA): SMS TOTP apps Push notifications FIDO2 keys.",
            "day_3": "SSO & Identity Protocols: SAML OAuth 2.0 OpenID Connect basics.",
            "day_4": "MFA Vulnerabilities: SIM swapping MFA Fatigue attacks Adversary-in-the-Middle.",
            "day_5": "Policy Enforcement: Designing secure MFA deployment policies.",
            "reality_task": "Implement MFA rules and identify bypass vulnerabilities.",
            "complexity": "Advanced", "key_concepts": ["MFA", "identity protection"], "badge_opportunity": None
        },
        8: {
            "topic": "Encryption & Cryptography", "objective": "Learn hashing encryption and data integrity.",
            "day_1": "Cryptography Concepts: Symmetric (AES) vs Asymmetric Encryption (RSA/ECC).",
            "day_2": "Hashing Functions: MD5 SHA-256 collision resistance and salt.",
            "day_3": "Data States: Data at Rest Data in Transit Data in Use protection.",
            "day_4": "PKI & Certificates: SSL/TLS handshakes Certificate Authorities HTTPS.",
            "day_5": "Integrity Verification: Verifying checksums and digital signatures.",
            "reality_task": "Encrypt confidential files and verify integrity using hashes.",
            "complexity": "Advanced", "key_concepts": ["hashing", "encryption"], "badge_opportunity": "Encryption Specialist"
        },
        9: {
            "topic": "Monitoring & Incident Response", "objective": "Learn operational monitoring and response workflows.",
            "day_1": "Vulnerability Scanning: Running scans using OpenVAS / Nessus concepts.",
            "day_2": "Incident Response Lifecycle: Preparation Detection Analysis Containment Eradication Recovery.",
            "day_3": "Log Aggregation: Intro to SIEM concepts (Splunk / Elastic stack).",
            "day_4": "Security Reporting: Writing technical findings vs executive summary.",
            "day_5": "Risk Prioritization: Remediation matrix based on vulnerability severity.",
            "reality_task": "Run vulnerability scans and prepare a security risk report.",
            "complexity": "Advanced", "key_concepts": ["vulnerability scans", "monitoring"], "badge_opportunity": None
        },
        10: {
            "topic": "Disaster Recovery Fundamentals", "objective": "Learn business continuity and recovery planning.",
            "day_1": "Business Continuity Planning (BCP) & Disaster Recovery (DR) concepts.",
            "day_2": "Recovery Metrics: RTO (Recovery Time Objective) & RPO (Recovery Point Objective).",
            "day_3": "Ransomware Mechanics: Encryption behavior C2 communication persistence.",
            "day_4": "Backup Strategies: 3-2-1 backup rule immutable backups air-gapping.",
            "day_5": "Incident Containment: Network isolation procedures during active breaches.",
            "reality_task": "Respond to a simulated ransomware attack.",
            "complexity": "Advanced", "key_concepts": ["ransomware", "disaster recovery"], "badge_opportunity": "Incident Responder"
        },
        11: {
            "topic": "Security Reporting & Documentation", "objective": "Learn professional reporting and portfolio preparation.",
            "day_1": "Technical Documentation: System baseline security configurations.",
            "day_2": "Standard Operating Procedures (SOPs): Writing Incident Response playbooks.",
            "day_3": "Executive Summaries: Explaining technical risk to non-technical leaders.",
            "day_4": "Evidence Handling: Chain of custody and forensic documentation rules.",
            "day_5": "Portfolio Assembly: Structuring security projects and audit reports.",
            "reality_task": "Compile vulnerability findings into a professional report.",
            "complexity": "Advanced", "key_concepts": ["reporting", "vulnerability documentation"], "badge_opportunity": None
        },
        12: {
            "topic": "Boardroom Defense & Risk Communication", "objective": "Learn stakeholder communication and strategic defense.",
            "day_1": "Security ROI: Translating security spend into risk mitigation dollars.",
            "day_2": "Presenting Risk Matrices: Impact vs Likelihood scoring for board members.",
            "day_3": "Handling Executive Pushback: Justifying security controls vs usability friction.",
            "day_4": "Slide Deck Design: Executive cyber risk presentation decks.",
            "day_5": "Defense Practice: Presenting risk mitigation plans under questioning.",
            "reality_task": "Present a cybersecurity risk mitigation plan to Sola.",
            "complexity": "Expert", "key_concepts": ["risk mitigation", "stakeholder communication"], "badge_opportunity": None
        },
        13: {
            "topic": "Advanced Network Security", "objective": "Learn IDS/IPS systems and secure architectures.",
            "day_1": "Intrusion Detection & Prevention (IDS/IPS): Signature vs Anomaly-based rules.",
            "day_2": "Packet Capture Analysis: Inspecting PCAP files with Wireshark.",
            "day_3": "Network Segmentation & Microsegmentation: Zero Trust network concepts.",
            "day_4": "VPNs & Secure Proxies: IPsec OpenVPN SSH Tunnels Reverse Proxies.",
            "day_5": "Suspicious Pattern Detection: Spotting beaconing data exfiltration port scans.",
            "reality_task": "Detect and isolate suspicious traffic patterns.",
            "complexity": "Expert", "key_concepts": ["IDS/IPS", "secure architectures"], "badge_opportunity": None
        },
        14: {
            "topic": "Ethical Hacking Fundamentals", "objective": "Learn penetration testing concepts safely.",
            "day_1": "Penetration Testing Phases: Reconnaissance Scanning Gaining Access Maintaining Access.",
            "day_2": "Reconnaissance: OSINT (Open Source Intelligence) Nmap port scanning strategies.",
            "day_3": "Web App Recon: Directory busting (gobuster/ffuf) banner grabbing.",
            "day_4": "Exploitation Mechanics: Understanding proof-of-concept exploits safely.",
            "day_5": "Remediation Verification: Re-testing systems after vulnerability patches.",
            "reality_task": "Identify vulnerabilities in a simulated web application.",
            "complexity": "Expert", "key_concepts": ["pentesting", "vulnerability scanning"], "badge_opportunity": "Vulnerability Analyst"
        },
        15: {
            "topic": "Web Application Security", "objective": "Learn OWASP Top 10 vulnerabilities and prevention.",
            "day_1": "OWASP Top 10 Intro: Broken Access Control Cryptographic Failures.",
            "day_2": "Injection Attacks: SQL Injection (SQLi) concepts testing and prevention.",
            "day_3": "Cross-Site Scripting (XSS): Stored Reflected DOM-based XSS mitigation.",
            "day_4": "Authentication Weaknesses: Session hijacking CSRF insecure direct object references (IDOR).",
            "day_5": "Web App Patching: Input sanitization parameterized queries WAF implementation.",
            "reality_task": "Patch vulnerabilities causing login exploitation.",
            "complexity": "Expert", "key_concepts": ["OWASP", "web vulnerabilities"], "badge_opportunity": None
        },
        16: {
            "topic": "Device & Endpoint Protection", "objective": "Learn endpoint monitoring and malware defense.",
            "day_1": "Endpoint Detection & Response (EDR) vs Antivirus (AV).",
            "day_2": "Malware Types: Trojans Keyloggers Rootkits Spyware behavior.",
            "day_3": "Host Logs: Auditing Windows Event Logs (Sysmon) and Linux Syslog.",
            "day_4": "Persistence Mechanisms: Registry keys scheduled tasks startup scripts.",
            "day_5": "Malware Containment: Isolating compromised hosts and memory extraction basics.",
            "reality_task": "Investigate malware infection across employee devices.",
            "complexity": "Expert", "key_concepts": ["endpoint monitoring", "malware defense"], "badge_opportunity": None
        },
        17: {
            "topic": "Cloud & Infrastructure Security", "objective": "Learn cloud security concepts and configurations.",
            "day_1": "Shared Responsibility Model: IaaS PaaS SaaS security boundaries.",
            "day_2": "Cloud Identity (IAM): Least privilege roles policies and service accounts.",
            "day_3": "Cloud Storage Security: Securing AWS S3 / Azure Blobs access policies.",
            "day_4": "Infrastructure as Code (IaC) Auditing: Misconfiguration scanning in cloud setups.",
            "day_5": "Cloud Logging & Auditing: AWS CloudTrail / GuardDuty event monitoring.",
            "reality_task": "Secure a misconfigured cloud storage bucket leaking files.",
            "complexity": "Expert", "key_concepts": ["cloud security", "storage buckets"], "badge_opportunity": None
        },
        18: {
            "topic": "SOC Workflows & Threat Hunting", "objective": "Learn SOC operations and threat detection.",
            "day_1": "SOC Operations: Tier 1 Tier 2 Tier 3 analyst roles and escalation pathways.",
            "day_2": "Threat Hunting Basics: Hypothesis-driven hunting using MITRE ATT&CK framework.",
            "day_3": "SIEM Querying: Writing detection queries in Splunk (SPL) or Elastic (KQL).",
            "day_4": "Correlation Rules: Building alerts for impossible travel pass-the-hash attacks.",
            "day_5": "False Positive Reduction: Tuning SIEM alerts to minimize fatigue.",
            "reality_task": "Investigate suspicious login behavior across multiple regions.",
            "complexity": "Expert", "key_concepts": ["SOC", "threat hunting"], "badge_opportunity": "SOC Operator"
        },
        19: {
            "topic": "Security Policies & Compliance", "objective": "Learn governance risk and compliance frameworks.",
            "day_1": "Compliance Frameworks: ISO 27001 NIST Cybersecurity Framework (CSF) SOC 2.",
            "day_2": "Data Privacy Regulations: GDPR NDPR HIPAA overview and obligations.",
            "day_3": "Security Policy Drafting: Acceptable Use Policy (AUP) Password Policy.",
            "day_4": "Third-Party Vendor Risk Management: Assessing vendor security posture.",
            "day_5": "Compliance Incident Auditing: Handling regulatory notification requirements.",
            "reality_task": "Draft a compliance response after a customer data exposure.",
            "complexity": "Expert", "key_concepts": ["governance", "compliance"], "badge_opportunity": "Compliance Guardian"
        },
        20: {
            "topic": "Security Automation & AI Risks", "objective": "Learn automated defense systems and AI threats.",
            "day_1": "Security Orchestration Automation and Response (SOAR) principles.",
            "day_2": "Python Scripting for Defense: Automating IP blocking and log parsing.",
            "day_3": "Automated Alert Workflows: Integrating SIEM alerts with Slack/Teams via Webhooks.",
            "day_4": "AI Security Risks: Prompt Injection Data Poisoning Model Inversion.",
            "day_5": "AI in Cyber Defense: Automated threat intelligence synthesis.",
            "reality_task": "Build an automated alert workflow for suspicious activity.",
            "complexity": "Expert", "key_concepts": ["automation", "AI threats"], "badge_opportunity": None
        },
        21: {
            "topic": "Enterprise Incident Management", "objective": "Learn coordinated enterprise-level response workflows.",
            "day_1": "Major Incident Command: Roles of Incident Commander Tech Lead Comms Lead.",
            "day_2": "Enterprise Breach Scenarios: Lateral movement Active Directory compromise.",
            "day_3": "Multi-System Isolation: Executing enterprise network containment strategies.",
            "day_4": "External Escalation: Engaging forensics vendors legal team law enforcement.",
            "day_5": "Post-Incident Root Cause Analysis: Creating Blameless Post-Mortem reports.",
            "reality_task": "Coordinate a response to a multi-system security breach.",
            "complexity": "Expert", "key_concepts": ["enterprise breach", "coordination"], "badge_opportunity": "Crisis Commander"
        },
        22: {
            "topic": "Attack & Defense Simulation", "objective": "Learn offensive vs defensive operations.",
            "day_1": "Red Team Tactics: Adversary Emulation Evasion techniques C2 infrastructure.",
            "day_2": "Blue Team Defenses: Hardening systems active threat hunting perimeter blockages.",
            "day_3": "Purple Team Collaboration: Bridging gaps between offense findings & defense rules.",
            "day_4": "Live Attack Mitigation: Detecting live intrusion simulation signals.",
            "day_5": "Post-Simulation Debrief: Documenting attack vectors and missed detections.",
            "reality_task": "Defend company infrastructure during a live attack simulation.",
            "complexity": "Expert", "key_concepts": ["attack simulation", "defense operations"], "badge_opportunity": None
        },
        23: {
            "topic": "Security Operations Management", "objective": "Learn prioritization escalation and team workflows.",
            "day_1": "Incident Prioritization: Triage protocols during high-volume alert spikes.",
            "day_2": "Resource Management: Managing analyst burnout and shift handoffs.",
            "day_3": "Operational Metrics: Mean Time to Detect (MTTD) Mean Time to Respond (MTTR).",
            "day_4": "Crisis Escalations: Deciding when to notify the C-Suite vs handling internally.",
            "day_5": "Team Playbook Updates: Refining Incident Response SOPs from lessons learned.",
            "reality_task": "Manage multiple simultaneous security incidents under pressure.",
            "complexity": "Expert", "key_concepts": ["prioritization", "escalation"], "badge_opportunity": None
        },
        24: {
            "topic": "Executive Boardroom Defense", "objective": "Learn strategic cybersecurity communication and leadership.",
            "day_1": "12-Month Security Roadmap: Defining security architecture and team scaling.",
            "day_2": "Justifying Security Investments: Proving value of tools SIEM and headcount.",
            "day_3": "Executive Deck Preparation: Creating clear high-impact security slides.",
            "day_4": "Mock Board Defense: Answering intense C-suite questions on business risk.",
            "day_5": "Final Review: Polishing strategy deck documentation and portfolio.",
            "reality_task": "Present a 12-month cybersecurity strategy to the executive board and justify security investments.",
            "complexity": "Expert", "key_concepts": ["strategy", "leadership"], "badge_opportunity": "Cyber Defense Certified"
        }
    }
}

def get_curriculum_step(track: str, task_number: int):
    """
    Retrieve the specific curriculum step for a given track and task number.
    Injects dynamic gamification identity based on the task_number (week).
    """
    track_key = str(track).lower().replace("-", "_").replace(" ", "_")
    print(f"DEBUG: Frontend sent track '{track}'. Normalized to '{track_key}'")

    track_curriculum = CURRICULUM.get(track_key, {})
    step_data = track_curriculum.get(task_number)
    
    if step_data:
        step_data["current_identity"] = get_identity_for_week(track_key, task_number)
        
    print(f"fetched curriculum step for {track_key} week {task_number}: -->", step_data)
    return step_data


# ============================================================
# PROGRESSION & BADGE ENGINE (UPDATED FOR GRADING GATE)
# ============================================================

def process_task_completion(supabase_client, user_id, track: str, current_week: int, score: int, attempt_number: int = 1, score_breakdown: dict = None):
    """
    Evaluates the student's score, awards badges, updates task scores, and executes Catch-Up logic.
    """
    if score_breakdown is None:
        score_breakdown = {}
        
    track_key = track.lower().replace(" ", "_").replace("-", "_")
    
    passed = (score >= 50) or (attempt_number >= 3)

    curriculum_step = CURRICULUM.get(track_key, {}).get(current_week, {})
    badge_to_award = curriculum_step.get("badge_opportunity")

    try:
        supabase_client.table("tasks").update({
            "score": score,
            "score_breakdown": score_breakdown,
            "status": "passed" if passed else "needs_revision",
            "completed": passed
        }).eq("user", user_id).eq("task_track", track).eq("week", current_week).execute()
        
    except Exception as e:
        print(f"Failed to update task scoring records: {e}")

    prog_response = supabase_client.table("user_progression").select("*").eq("user_id", user_id).execute()
    existing_prog = prog_response.data[0] if prog_response.data else {}
    
    exc_count = existing_prog.get("excellent_count", 0)
    gd_count = existing_prog.get("good_count", 0)
    pass_count = existing_prog.get("pass_count", 0)

    if passed:
        print(f"✅ User {user_id} scored {score} (Attempt {attempt_number}). Evaluating progression timeline...")

        if score >= 85: exc_count += 1
        elif score >= 70: gd_count += 1
        else: pass_count += 1

        expected_week = current_week
        try:
            created_at_str = existing_prog.get("created_at", datetime.datetime.utcnow().isoformat())
            created_at = parser.isoparse(created_at_str).replace(tzinfo=None)
            days_active = (datetime.datetime.utcnow() - created_at).days
            expected_week = (days_active // 7) + 1
        except Exception as e:
            print(f"⚠️ Expected week calculation failed: {e}")

        if expected_week > current_week and current_week < 24:
            next_week = current_week + 1
            new_identity = get_identity_for_week(track_key, next_week)
            
            progression_data = {
                "user_id": user_id,
                "current_week": next_week,
                "current_identity": new_identity,
                "week_status": "in_progress",
                "excellent_count": exc_count,
                "good_count": gd_count,
                "pass_count": pass_count,
                "updated_at": datetime.datetime.utcnow().isoformat()
            }
            supabase_client.table("user_progression").upsert(progression_data).execute()
            print(f"⚡ CATCH-UP TRIGGERED! User {user_id} progressed to Week {next_week}.")

        else:
            new_identity = get_identity_for_week(track_key, current_week)
            progression_data = {
                "user_id": user_id,
                "current_week": current_week,
                "current_identity": new_identity,
                "week_status": "passed_waiting",
                "excellent_count": exc_count,
                "good_count": gd_count,
                "pass_count": pass_count,
                "updated_at": datetime.datetime.utcnow().isoformat()
            }
            supabase_client.table("user_progression").upsert(progression_data).execute()
            print(f"🔒 User {user_id} is on schedule. Marked as 'passed_waiting'.")

        if badge_to_award:
            badge_data = {
                "user_id": user_id,
                "badge_name": badge_to_award,
                "earned_in_week": current_week
            }
            try:
                supabase_client.table("user_badges").insert(badge_data).execute()
                print(f"🎉 Successfully awarded '{badge_to_award}' badge to user {user_id}!")
            except Exception as e:
                print(f"Badge '{badge_to_award}' already exists or an error occurred: {e}")

    else:
        progression_data = {
            "user_id": user_id,
            "current_week": current_week,
            "week_status": "needs_revision",
            "updated_at": datetime.datetime.utcnow().isoformat()
        }
        supabase_client.table("user_progression").upsert(progression_data).execute()
        print(f"❌ User {user_id} scored {score} (<50). Marked as 'needs_revision'.")

    return passed