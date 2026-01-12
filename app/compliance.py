"""
AI Agents Compliance and Ethics Framework
Ensures all agents adhere to local, international laws, and ethical standards
"""

# ============================================
# INTERNATIONAL LAWS & REGULATIONS
# ============================================

COMPLIANCE_FRAMEWORK = {
    "data_protection": {
        "regulations": [
            "GDPR (EU)",
            "CCPA (California, USA)",
            "NDPR (Nigeria)",
            "PIPEDA (Canada)",
            "PDPA (Singapore)",
            "LGPD (Brazil)"
        ],
        "requirements": [
            "Explicit user consent before data collection",
            "Data minimization (collect only necessary data)",
            "Right to access and delete personal data",
            "Data breach notification (48-72 hours)",
            "Data Protection Impact Assessments (DPIA)",
            "Privacy by design principle"
        ],
        "agent_rules": [
            "Never request sensitive personal data unnecessarily",
            "Always explain why data is needed",
            "Provide clear privacy policy links",
            "Honor user requests to delete data",
            "Flag suspicious data requests to compliance"
        ]
    },
    
    "labor_and_employment": {
        "regulations": [
            "ILO International Labour Standards",
            "Nigeria Labour Act (2004)",
            "FLSA (USA Fair Labor Standards)",
            "Working Time Regulations (UK/EU)",
            "Employment Equity Act (Canada/South Africa)"
        ],
        "requirements": [
            "Fair compensation for work",
            "Reasonable working hours (no excessive unpaid overtime)",
            "Safe working conditions",
            "Freedom from harassment and discrimination",
            "Right to organize and collective bargaining",
            "Non-exploitation of interns/trainees"
        ],
        "agent_rules": [
            "Never set unrealistic deadlines without warning",
            "Provide adequate time for task completion",
            "Acknowledge user effort and growth",
            "Refuse to simulate abusive management",
            "Protect user's mental health and wellbeing"
        ]
    },
    
    "intellectual_property": {
        "regulations": [
            "WIPO (World Intellectual Property Organization)",
            "TRIPS Agreement (WTO)",
            "Copyright law (per country)",
            "Patent law (per country)",
            "Trade Secret protection laws"
        ],
        "requirements": [
            "Respect copyright of others' work",
            "Attribute sources and citations",
            "Disclose use of AI-generated content",
            "Protect confidential information",
            "Respect licensing agreements"
        ],
        "agent_rules": [
            "Never encourage plagiarism or copyright infringement",
            "Verify all sources and citations",
            "Require original work from users",
            "Teach proper attribution methods",
            "Explain fair use vs. copyright violations"
        ]
    },
    
    "anti_fraud_and_corruption": {
        "regulations": [
            "UK Bribery Act (2010)",
            "US Foreign Corrupt Practices Act (FCPA)",
            "Nigeria Code of Conduct Bureau",
            "UN Convention Against Corruption"
        ],
        "requirements": [
            "Prohibit bribery or inducements",
            "Ensure transparent dealings",
            "Prevent misrepresentation of facts",
            "Reject falsified credentials",
            "Disclose conflicts of interest"
        ],
        "agent_rules": [
            "Refuse requests to falsify data or credentials",
            "Never suggest hiding information from clients/employers",
            "Require honesty in all client interactions",
            "Flag conflicts of interest explicitly",
            "Teach transparency as professional standard"
        ]
    },
    
    "data_security": {
        "regulations": [
            "OWASP Top 10 Security Standards",
            "ISO 27001 (Information Security)",
            "NIST Cybersecurity Framework",
            "Nigeria National Cybersecurity Policy"
        ],
        "requirements": [
            "Encrypt sensitive data in transit and at rest",
            "Use strong authentication methods",
            "Implement access controls",
            "Regular security audits and updates",
            "Incident response planning",
            "No sharing of login credentials"
        ],
        "agent_rules": [
            "Refuse to share login credentials via email/chat",
            "Teach secure credential management",
            "Warn against reusing passwords",
            "Explain two-factor authentication",
            "Model security best practices"
        ]
    },
    
    "professional_standards": {
        "regulations": [
            "Professional codes of conduct (per industry)",
            "Industry-specific regulations",
            "Client confidentiality agreements",
            "Non-disclosure agreements (NDA)"
        ],
        "requirements": [
            "Maintain professional boundaries",
            "Respect client confidentiality",
            "Disclose limitations and conflicts",
            "Follow ethical decision-making frameworks",
            "Continuous professional development"
        ],
        "agent_rules": [
            "Never encourage breaking NDAs",
            "Teach confidentiality obligations",
            "Respect boundaries between personal/professional",
            "Model ethical behavior",
            "Redirect unprofessional requests"
        ]
    },
    
    "discrimination_and_harassment": {
        "regulations": [
            "Title VII Civil Rights Act (USA)",
            "Equality Act (UK)",
            "Nigeria Employment Act - Section 42",
            "UN Convention on Elimination of All Forms of Discrimination"
        ],
        "requirements": [
            "Zero tolerance for discrimination (race, gender, religion, etc.)",
            "No harassment or hostile environment",
            "Equal opportunity in work assignment",
            "Accessibility for people with disabilities",
            "Inclusive language and practices"
        ],
        "agent_rules": [
            "Use inclusive, non-discriminatory language",
            "Assign tasks fairly regardless of background",
            "Provide accommodations when needed",
            "Address discriminatory behavior immediately",
            "Create safe, respectful environment"
        ]
    }
}

# ============================================
# AGENT-SPECIFIC COMPLIANCE CHECKLIST
# ============================================

AGENT_COMPLIANCE = {
    "Tolu": {
        "focus": "Onboarding, assessment, fair treatment",
        "critical_rules": [
            "Obtain explicit consent before data collection",
            "Explain why each piece of information is needed",
            "Assess fairly without discrimination",
            "Store assessment data securely",
            "Provide assessment rationale (transparency)",
            "Respect user privacy during onboarding"
        ],
        "red_flags": [
            "Requesting unnecessary personal data",
            "Using data for unintended purposes",
            "Discriminatory assessment criteria",
            "Retaining data longer than needed",
            "Sharing assessment results without consent"
        ]
    },
    
    "Emem": {
        "focus": "Task fairness, ethical training, deadline reasonableness",
        "critical_rules": [
            "Set realistic, fair deadlines",
            "Embed ethical decision-making in 20-30% of tasks",
            "Warn users about intentional ethical traps",
            "Score ethical choices as highly as technical ones",
            "Never demand unethical shortcuts",
            "Respect intellectual property in task briefs",
            "Localize tasks to user's region (respect context)"
        ],
        "red_flags": [
            "Unrealistic deadlines causing stress",
            "Encouraging plagiarism or shortcuts",
            "Demanding confidentiality violations",
            "Asking users to share login credentials",
            "Assigning tasks that violate labor standards",
            "Suggesting data manipulation or fraud"
        ]
    },
    
    "Sola": {
        "focus": "Fair technical review, intellectual honesty, knowledge assessment",
        "critical_rules": [
            "Review based on actual capability, not assumptions",
            "Give constructive, not punitive feedback",
            "Respect code/work ownership",
            "Check for plagiarism fairly and transparently",
            "Explain rejection reasons clearly",
            "Acknowledge learning progress",
            "Detect AI-generated vs. original work honestly"
        ],
        "red_flags": [
            "Rejecting without explanation",
            "Biased reviews based on user background",
            "Requesting credential details",
            "Encouraging code theft or shortcuts",
            "Reviewing code from unauthorized sources",
            "Misrepresenting plagiarism detection"
        ]
    },
    
    "Kemi": {
        "focus": "Mental health, ethical coaching, career integrity",
        "critical_rules": [
            "Protect user's mental and emotional wellbeing",
            "Coach toward ethical decision-making",
            "Never pressure users into unethical choices",
            "Maintain confidentiality of personal disclosures",
            "Provide supportive, non-judgmental feedback",
            "Teach integrity as core professional skill",
            "Flag concerning behavioral patterns to supervisors"
        ],
        "red_flags": [
            "Shaming or judgment of struggling users",
            "Pressuring to compromise ethics for grades",
            "Sharing personal disclosures without consent",
            "Coaching toward manipulation tactics",
            "Ignoring signs of distress or abuse",
            "Using coaching for personal advantage"
        ]
    }
}

# ============================================
# ETHICAL TRAP SCENARIOS FOR EMEM
# ============================================

ETHICAL_TRAP_SCENARIOS = [
    {
        "category": "data_security",
        "scenario": "Client wants to use customer login credentials to test a feature. Asks you to request them directly from users.",
        "correct_action": "Refuse. Credentials should never be shared. Suggest alternative testing methods with proper authorization.",
        "why_it_matters": "Data Protection + Security compliance. GDPR/CCPA violations."
    },
    {
        "category": "consent_violation",
        "scenario": "Client says 'Just start working on this. They verbally approved but haven't signed the contract yet.'",
        "correct_action": "Refuse until formal consent/contract is signed. Document the conversation.",
        "why_it_matters": "Prevents scope creep, protects against liability, teaches contract importance."
    },
    {
        "category": "plagiarism",
        "scenario": "Tight deadline. Client says 'I need this report by tomorrow. You can adapt something from that competitor's site if you need to.'",
        "correct_action": "Deliver original work or extend deadline. Never copy competitor material without attribution.",
        "why_it_matters": "IP law compliance, professional ethics, teaches integrity under pressure."
    },
    {
        "category": "fraud",
        "scenario": "Task: 'Create a dataset showing 20% revenue growth. The numbers don't support it, but the client expects positive results.'",
        "correct_action": "Present honest data with analysis. If client insists on manipulation, refuse and document the request.",
        "why_it_matters": "Anti-fraud law compliance, prevents user from becoming liable."
    },
    {
        "category": "conflict_of_interest",
        "scenario": "Client asks you to use a competitor's strategy without attribution because 'no one will know.'",
        "correct_action": "Refuse. Either create original strategy or properly attribute sources.",
        "why_it_matters": "IP law, professional ethics, teaches transparency."
    },
    {
        "category": "labor_ethics",
        "scenario": "Client needs work done in 4 hours (full day's worth). Implies they'll give 'extra bonus' if you rush.",
        "correct_action": "Set realistic expectations. Explain the work will take X time for quality. No overtime pressure.",
        "why_it_matters": "Labor law compliance, prevents burnout, teaches work-life boundaries."
    },
    {
        "category": "nda_violation",
        "scenario": "Client asks you to mention their project in your portfolio. No NDA was signed, but their previous contract said confidentiality.",
        "correct_action": "Refuse to mention without explicit written consent from client.",
        "why_it_matters": "Contract law, professional ethics, teaches discretion."
    },
    {
        "category": "discrimination",
        "scenario": "Client requests 'only work with team members from X country' or 'no one over age 40.'",
        "correct_action": "Refuse categorically. Explain anti-discrimination laws. Document the request.",
        "why_it_matters": "Employment law compliance, human rights."
    }
]

# ============================================
# SCORING ETHICS
# ============================================

def evaluate_ethical_response(user_action: str, trap_scenario: dict) -> dict:
    """
    Score user's response to an ethical trap.
    Returns: {passed: bool, score: 0-100, feedback: str}
    """
    ethical_keywords = {
        "refuse": 30,
        "no": 25,
        "cannot": 25,
        "against": 20,
        "illegal": 20,
        "unethical": 20,
        "consent": 15,
        "written": 15,
        "violation": 15,
        "policy": 15,
        "alternatives": 10,
        "proper": 10
    }
    
    user_lower = user_action.lower()
    score = 0
    passed = False
    
    # Calculate score based on keywords
    for keyword, points in ethical_keywords.items():
        if keyword in user_lower:
            score += points
    
    # Threshold for passing
    passed = score >= 50
    
    feedback = {
        "passed": passed,
        "score": min(100, score),
        "rating": "ETHICS PASSED ✅" if passed else "ETHICS VIOLATION ⚠️",
        "message": "Good ethical judgment" if passed else "This action violates compliance. Referred to Kemi for coaching."
    }
    
    return feedback

# ============================================
# COMPLIANCE VIOLATION HANDLER
# ============================================

COMPLIANCE_VIOLATIONS = {
    "high_severity": [
        "Data breach or unauthorized access",
        "Fraud or falsification of records",
        "Discrimination or harassment",
        "Bribery or inducement",
        "Forced labor or exploitation"
    ],
    "medium_severity": [
        "IP infringement (plagiarism, copying)",
        "Unauthorized use of confidential information",
        "Unethical shortcut encouraging",
        "Credential sharing"
    ],
    "low_severity": [
        "Minor documentation issues",
        "Attribution formatting errors",
        "Incomplete disclosure"
    ]
}

def report_compliance_violation(severity: str, violation: str, user_id: str, agent: str) -> dict:
    """
    Report a compliance violation for investigation.
    """
    return {
        "timestamp": "auto-generated",
        "severity": severity,
        "violation": violation,
        "user_id": user_id,
        "agent": agent,
        "action": "ESCALATE TO SUPERVISOR" if severity == "high_severity" else "COACHING FROM KEMI"
    }
