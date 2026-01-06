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


async def translate_to_cv_bullet(
    task_title: str,
    task_description: str,
    user_accomplishment: str,
    model: genai.GenerativeModel
) -> dict:
    """
    Translate a completed task into a professional CV bullet point.
    
    Returns:
        dict with skill_tag and bullet_point
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
    
    user_level = context.get("user_level", "Unknown")
    track = context.get("track", "Unknown")
    
    prompt = f"""
{system_prompt}

---

**CONTEXT:**
User Level: {user_level}
Track: {track}

**RECENT CHAT:**
{history_text}

**USER MESSAGE:**
{message}

Respond as Coach Kemi. Be warm, encouraging, and focus on their growth.
If they're struggling, help them see the bigger picture.
If they're celebrating, celebrate with them and remind them of their progress.
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
    model: genai.GenerativeModel
) -> dict:
    """
    Conduct a mock interview session.
    
    interview_type: 'behavioral', 'technical', 'situational'
    
    Returns:
        dict with question, follow_up (if applicable), tip
    """
    system_prompt = get_system_prompt()
    
    prompt = f"""
{system_prompt}

---

**MOCK INTERVIEW SESSION**
Type: {interview_type}
Question Number: {question_number}
{"Previous Answer: " + previous_answer if previous_answer else "This is the first question."}

{"If they provided an answer, briefly evaluate it (1 sentence) then ask a follow-up or next question." if previous_answer else ""}

Generate an interview question appropriate for an entry-level tech role.
Be professional - this is practice for real interviews.

Respond with JSON:
{{
    "evaluation": "Brief feedback on previous answer (if applicable)",
    "question": "The interview question",
    "tip": "A brief tip for answering this type of question"
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
            "question": "Tell me about a time you faced a challenging deadline.",
            "tip": "Use the STAR method: Situation, Task, Action, Result"
        }
