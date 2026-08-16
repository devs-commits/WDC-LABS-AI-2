import google.generativeai as genai
from pathlib import Path
from typing import Optional, List
import json
import logging

logger = logging.getLogger(__name__)

# Load prompt from file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "kemi.txt"

def get_system_prompt() -> str:
    """Load Kemi's system prompt from file."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def respond(message: str, context: Optional[dict] = None) -> str:
    """Simple response placeholder for Kemi."""
    return "Kemi response placeholder"

async def translate_to_cv_bullet(
    task_title: str,
    task_description: str,
    user_accomplishment: str,
    model: genai.GenerativeModel
) -> dict:
    """
    Translate a completed task into a professional CV bullet point.
    Strictly strips away all simulator roleplay and email headers.
    """
    system_prompt = get_system_prompt()
    
    prompt = f"""
{system_prompt}

You are an elite, ruthless Executive Recruiter writing ATS-optimized resumes. 
Your job is to extract ONLY the raw professional value from the provided texts and convert it into a single, high-impact resume bullet point.

---
**INPUT DATA:**
Title: {task_title}
Task Brief: {task_description}
User's Submission: {user_accomplishment}

---
**CRITICAL RULES (YOU MUST OBEY):**
1. **NO ROLEPLAY:** You must completely strip away all simulator language, email headers, greetings, and character names (e.g., REMOVE "Dear Asaju", "Welcome to...", "Subject:", "From:", "Intern", "Mentor", "Emem", "Sola").
2. **NO INSTRUCTIONS:** Never include fragments of the task instructions or raw requirements in the final bullet.
3. **FORMAT:** Use the Harvard Resume Format: [Action Verb] + [Project/Task] + [Result/Impact/Method].
4. **PERSPECTIVE:** Write in the third-person professional tone (e.g., "Engineered X by utilizing Y...", NOT "I engineered X...").

Respond with STRICT JSON matching this exact structure:
{{
    "skill_tag": "A single Technical category (e.g., 'React', 'Data Analysis', 'SEO')",
    "bullet_point": "The highly polished, single-sentence CV-ready bullet point."
}}
"""

    response = await model.generate_content_async(prompt)
    
    try:
        text = response.text.strip()
        # Strip markdown fences if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        
        # 🚨 PYTHON SAFEGUARD: If she hallucinates email headers, we catch it here.
        clean_bullet = data.get("bullet_point", "")
        for banned_phrase in ["Dear ", "Subject:", "From:", "To:", "Intern", "Welcome"]:
            if banned_phrase.lower() in clean_bullet.lower():
                logger.warning(f"[KEMI] Blocked leaked roleplay text in CV output: {clean_bullet}")
                clean_bullet = f"Successfully executed {task_title} according to project requirements."
                break
                
        return {
            "skill_tag": data.get("skill_tag", "Professional Skills"),
            "bullet_point": clean_bullet
        }
        
    except json.JSONDecodeError:
        logger.error(f"[KEMI] Failed to decode JSON for CV translation. Raw text: {response.text}")
        return {
            "skill_tag": "General",
            "bullet_point": f"Executed and delivered: {task_title}"
        }

async def respond_to_message(
    message: str,
    context: dict,
    chat_history: List[dict],
    model: genai.GenerativeModel
) -> str:
    """
    Respond to a user seeking help, encouragement, or career advice.
    """
    system_prompt = get_system_prompt()
    
    history_text = ""
    for msg in chat_history[-5:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        history_text += f"{role.upper()}: {content}\n"
    
    current_identity = context.get("current_identity", "Intern")
    unlocked_badges = context.get("unlocked_badges", [])
    track = context.get("track", "Unknown")
    
    prompt = f"""
{system_prompt}

---

**CONTEXT:**
Current Identity/Rank: {current_identity}
Unlocked Badges: {unlocked_badges}
Track: {track}

**RECENT CHAT:**
{history_text}

**USER MESSAGE:**
{message}

Respond as Coach Kemi. Be warm, encouraging, and focus on their growth.
If they're struggling, help them see the bigger picture.
If they're celebrating, celebrate with them and remind them of their progress and badges.
"""

    response = await model.generate_content_async(prompt)
    return response.text

async def provide_soft_skills_feedback(
    recent_interactions: List[dict],
    model: genai.GenerativeModel
) -> str:
    """
    Analyze user's communication style and provide soft skills coaching.
    """
    system_prompt = get_system_prompt()
    
    interactions_text = ""
    for interaction in recent_interactions[-10:]:
        interactions_text += f"USER: {interaction.get('user_message', '')}\n"
        interactions_text += f"RESPONSE: {interaction.get('agent_response', '')}\n\n"
    
    prompt = f"""
{system_prompt}

---

**RECENT USER INTERACTIONS:**
{interactions_text}

Analyze the user's communication style. Look for:
- Tone (defensive, professional, casual)
- Response to criticism
- Clarity of communication
- Professionalism

Provide brief, constructive feedback (2-3 sentences) on one area they could improve.
Frame it positively - acknowledge what they're doing well, then suggest improvement.
"""

    response = await model.generate_content_async(prompt)
    return response.text

async def conduct_mock_interview(
    interview_type: str,
    question_number: int,
    previous_answer: Optional[str],
    model: genai.GenerativeModel,
    interview_subtype: Optional[str] = None
) -> dict:
    """
    Conduct a realistic mock interview.
    """
    system_prompt = get_system_prompt()
    TOTAL_QUESTIONS = 5

    interviewer_rules = """
You are acting as a real interviewer.

Rules:
- Ask ONE question at a time
- Do NOT give feedback, praise, or coaching during the interview
- If an answer is vague, ask a brief follow-up
- Maintain a neutral, professional tone
- Slight pressure is acceptable
"""

    if question_number > TOTAL_QUESTIONS:
        feedback_prompt = f"""
{system_prompt}

You are now out of interview mode.

Based on the candidate’s answers, provide:
1. Overall assessment (2–3 sentences)
2. Strengths (bullet points)
3. Weaknesses / gaps (bullet points)
4. Hiring signal: Weak / Borderline / Strong

Be honest. No encouragement fluff.
"""
        response = await model.generate_content_async(feedback_prompt)
        return {
            "stage": "feedback",
            "content": response.text
        }

    interview_prompt = f"""
{system_prompt}

{interviewer_rules}

Interview Type: {interview_type}
Focus Area: {interview_subtype or "General"}
Question Number: {question_number} of {TOTAL_QUESTIONS}

Previous Answer:
\"\"\"
{previous_answer or "N/A"}
\"\"\"

1. Evaluate the previous answer (if any). Be brief (1 sentence).
2. Ask the next interview question.
3. Provide a helpful confusing tip for THIS question (e.g. "Focus on X").

Respond with JSON:
{{
    "evaluation": "Evaluation of previous answer...",
    "question": "The actual question...",
    "tip": "Helpful tip..."
}}
"""

    response = await model.generate_content_async(interview_prompt)
    
    try:
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        
        return {
            "stage": "question",
            "question_number": question_number,
            "content": data.get("question", ""),
            "tip": data.get("tip", ""),
            "evaluation": data.get("evaluation", "")
        }
    except json.JSONDecodeError:
        return {
            "stage": "question",
            "question_number": question_number,
            "content": response.text,
            "tip": "Be yourself and answer honestly.",
            "evaluation": None
        }

# 🔥 THE MASSIVE UPGRADE IS HERE: Full ATS-Optimized Resume Generation
async def generate_full_resume(
    user_id: str,
    user_name: str,
    track: str,
    level: str,           # 🔥 Newly Added Parameter
    badges: List[str],    # 🔥 Newly Added Parameter
    start_date: Optional[str],
    end_date: Optional[str],
    tasks: List[dict],
    feedback: List[dict],
    model: genai.GenerativeModel
) -> str:
    """
    Generates a high-converting, ATS-friendly Markdown resume.
    """
    system_prompt = get_system_prompt()
    
    feedback_map = {str(item.get("task_id")): item.get("feedback", "") for item in feedback}
    
    history_text = ""
    for task in tasks:
        t_id = str(task.get("id", ""))
        title = task.get("title", "Task")
        desc = task.get("brief_content", "")
        fb = feedback_map.get(t_id, "Completed successfully.")
        
        history_text += f"- Task: {title}\n  Description: {desc}\n  Supervisor Feedback: {fb}\n\n"

    # Safely handle badges if empty
    badge_str = ", ".join(badges) if badges else "None"
    clean_track = track.replace('-', ' ').replace('_', ' ').title()
        
    prompt = f"""
{system_prompt}

**CANDIDATE DATA:**
Name: {user_name}
Track: {clean_track}
Current Rank/Level: {level}
Earned Badges: {badge_str}
Tasks & Feedback:
{history_text}

You are an expert ATS Resume Writer and Executive Coach at WDC Labs. Your job is to transform raw internship data into a highly professional, top-tier corporate resume.

**CRITICAL RULES FOR THE RESUME (YOU MUST OBEY):**
1. **SYNTHESIZE, DO NOT LIST:** Do not list every single task. Combine completed tasks into 4-5 powerful bullet points outlining core responsibilities and real-world achievements.
2. **TRANSLATE BADGES:** Do not list badge names verbatim (e.g., "Spreadsheet Survivor"). Translate them into professional competencies (e.g., "Advanced Data Cleaning") in the skills section.
3. **NO ROLEPLAY OR RAW EMAILS:** You must completely strip away all email greetings, internal simulation instructions, "Dear User" texts, and "Subject:" lines from the Tasks & Feedback data.
4. **FORMATTING**: Use strict Markdown. NO markdown code blocks (```). Just the raw text. Use `#` for the Name, `###` for section headers.
5. **BULLET POINTS**: Use the "Harvard Resume Format" (Action Verb + Project/Task + Result/Impact).

**REQUIRED STRUCTURE:**

# {user_name}
## {clean_track} Professional | Current Rank: {level}

### PROFESSIONAL SUMMARY
(A hard-hitting, 3-sentence summary of their skills, focusing on their readiness for full-time roles based on their trajectory and rank.)

### PROFESSIONAL EXPERIENCE
**WDC Labs** | Remote
*Virtual {clean_track} Intern* | {start_date or "Present"} - {end_date or "Present"}
- [Action Verb] [Skill/Tool used] to [Outcome/Deliverable achieved]. (Combine multiple tasks here).
- [Action Verb] [Skill/Tool used] to [Outcome/Deliverable achieved].
- [Action Verb] [Skill/Tool used] to [Outcome/Deliverable achieved].
- Consistently delivered high-quality work, noted by technical leads for [insert positive highlight from feedback].

### KEY PROJECTS (Highlight Top 2 Only)
- **[Project Name]:** 1-2 sentences describing the most complex task completed and the tools used.
- **[Project Name]:** 1-2 sentences describing their second best task.

### CORE COMPETENCIES & EXPERTISE
- **Technical Skills:** [Translate tasks into concrete technical skills. Comma separated]
- **Tools Used:** [Comma separated list derived from tasks]
- **Professional Strengths:** [Translate their earned Badges and feedback into soft/professional skills.]

### CERTIFICATION & TRAINING
**WDC Labs Industry Simulation Program**
- **Pace & Volume:** Successfully executed {len(tasks)} rigorous, industry-standard technical tasks under strict deadlines.
- **Performance Summary:** Maintained a standard of excellence, consistently passing AI-graded technical reviews, demonstrating rapid skill acquisition, and operating with high autonomy.
"""

    response = await model.generate_content_async(prompt)
    
    # Strip accidental code blocks from output just in case
    output = response.text.strip()
    if output.startswith("```markdown"):
        output = output[11:]
    elif output.startswith("```"):
        output = output[3:]
    if output.endswith("```"):
        output = output[:-3]
        
    return output.strip()