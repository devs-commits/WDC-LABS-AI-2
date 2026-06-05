import google.generativeai as genai
from pathlib import Path
from typing import Optional, List
import json

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
    """
    system_prompt = get_system_prompt()
    
    prompt = f"""
{system_prompt}

---

**TASK COMPLETED:**
Title: {task_title}
Description: {task_description}

**WHAT THE USER DID:**
{user_accomplishment}

Translate this into a professional CV bullet point that would impress recruiters.
Use action verbs, quantify impact where possible, and highlight transferable skills.

Respond with JSON:
{{
    "skill_tag": "Technical category (e.g., 'SQL', 'Data Analysis', 'SEO')",
    "bullet_point": "The professional CV-ready bullet point"
}}
"""

    response = await model.generate_content_async(prompt)
    
    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return {
            "skill_tag": "General",
            "bullet_point": f"Successfully completed: {task_title}"
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
        
        # Strip markdown fences if present
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

async def generate_full_resume(
    user_id: str,
    user_name: str,
    track: str,
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
        
    prompt = f"""
{system_prompt}

**CANDIDATE DATA:**
Name: {user_name}
Track: {track}
Tasks & Feedback:
{history_text}

You are an elite Executive Recruiter writing a highly professional, ATS-optimized resume for this candidate based ONLY on their completed tasks. 

**RULES FOR THE RESUME:**
1. **Formatting**: Use strict Markdown. Use `#` for the Name, `###` for section headers.
2. **Tone**: Confident, highly professional, action-oriented.
3. **Bullet Points**: Use the "Harvard Resume Format" (Action Verb + Project/Task + Result/Impact). Infer the professional impact based on the Supervisor Feedback.

**REQUIRED STRUCTURE:**

# [Candidate Name]
**[Track Title e.g. Data Analyst / Cyber Security Specialist]**

---

### PROFESSIONAL SUMMARY
(Write a compelling 3-sentence summary highlighting their practical experience, number of completed simulations, and technical capabilities proven in WDC Labs.)

### TECHNICAL & CORE COMPETENCIES
(List 6-8 relevant skills as bullet points, derived from their tasks.)

### PROFESSIONAL EXPERIENCE
**WDC Labs** | *Virtual {track.replace('-', ' ').title()} Intern*
(Translate their tasks into 4-6 incredibly strong bullet points. Do not just list the task descriptions—reframe them as professional achievements. Example: "Engineered X by utilizing Y, resulting in Z (as verified by technical supervisor).")

### EDUCATION & CERTIFICATIONS
* **WDC Labs Immersive Career Program** - Certificate of Completion
* *[Add your personal Education here]*
"""

    response = await model.generate_content_async(prompt)
    return response.text