import google.generativeai as genai
from pathlib import Path
from typing import Optional, List
from app.archives.index import ARCHIVE_LIBRARY
import json

# Load prompt from file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "sola.txt"


def get_system_prompt() -> str:
    """Load Sola's system prompt from file."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def respond(message: str, context: dict | None = None) -> str:
    """Simple response placeholder for Sola."""
    return "Sola response placeholder"

def select_task_resources(task_brief: str, track: str) -> list:
    resources = []

    task_lower = task_brief.lower()

    for item in ARCHIVE_LIBRARY.get(track, []):
        if any(tag in task_lower for tag in item["tags"]):
            resources.append(item)

    # Always add one general workflow hint
    resources += ARCHIVE_LIBRARY.get("general", [])[:1]

    return resources[:3]  # hard limit


async def review_submission(
    task_title: str,
    task_brief: str,
    submission_content: str,
    client_constraints: Optional[str],
    model: genai.GenerativeModel
) -> dict:
    """
    Review a user's submission as Sola (Technical Lead).
    
    Implements the 60% Rejection Rule - rejects unless work is excellent.
    
    Returns:
        dict with feedback, passed (bool), score (0-100), improvement_points
    """
    system_prompt = get_system_prompt()
    
    prompt = f"""
{system_prompt}

---

**TASK TO REVIEW:**
Title: {task_title}
Brief: {task_brief}
Client Constraints: {client_constraints or "None specified"}

**USER'S SUBMISSION:**
\"\"\"
{submission_content}
\"\"\"

**REVIEW INSTRUCTIONS:**
1. Check if submission addresses the task requirements
2. Check code quality (if applicable): variable names, structure, comments
3. Check if client constraints were followed
4. Check formatting and professionalism
5. Apply the 60% Rejection Rule - only approve truly excellent work

Respond with JSON:
{{
    "feedback": "Your detailed feedback message",
    "passed": true | false,
    "score": 0-100,
    "improvement_points": ["Point 1", "Point 2"] // Only if failed
}}

Remember: You reject 60% of first drafts. Be thorough but fair.
"""

    response = await model.generate_content_async(prompt)
    
    # Parse JSON from response
    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        result = json.loads(text.strip())
        return result
    except json.JSONDecodeError:
        # Fallback - assume rejection if parsing fails
        return {
            "feedback": response.text,
            "passed": False,
            "score": 50,
            "improvement_points": ["Please resubmit with clearer formatting"]
        }


async def respond_to_message(
    message: str,
    context: dict,
    chat_history: List[dict],
    model: genai.GenerativeModel
) -> str:
    """
    Respond to a technical question as Sola using the Socratic method.
    """
    system_prompt = get_system_prompt()
    
    history_text = ""
    for msg in chat_history[-5:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        history_text += f"{role.upper()}: {content}\n"
    
    current_task = context.get("task_brief", "No active task")
    
    prompt = f"""
{system_prompt}

---

**CONTEXT:**
Current Task: {current_task}

**RECENT CHAT:**
{history_text}

**USER MESSAGE:**
{message}

Respond as Sola. Use the Socratic method - guide them with questions, don't give direct answers.
If they're asking about code/technical issues, ask clarifying questions that lead them to the solution.
"""

    response = await model.generate_content_async(prompt)
    return response.text


async def interrogate_submission(
    submission_content: str,
    approach_used: str,
    model: genai.GenerativeModel
) -> str:
    """
    The "Socratic Defense" - interrogate why the user made specific choices.
    This catches copied/AI-generated work since users can't defend choices they didn't make.
    """
    system_prompt = get_system_prompt()
    
    prompt = f"""
{system_prompt}

---

**USER'S SUBMISSION:**
{submission_content}

**THEIR STATED APPROACH:**
{approach_used}

Generate 2-3 pointed questions about their technical choices:
- Why did they choose this specific method/approach?
- Why not an alternative approach?
- Can they explain a specific line/section?

These questions should reveal whether they truly understand their work or just copied it.
Be professional but probing.
"""

    response = await model.generate_content_async(prompt)
    return response.text
