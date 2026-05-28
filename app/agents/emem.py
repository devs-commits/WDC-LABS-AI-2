import google.generativeai as genai
from pathlib import Path
from typing import Optional, List
from app.utils.deadline_formatter import format_deadline_display

# Load prompt from file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "emem.txt"

def get_system_prompt() -> str:
    """Load Emem's system prompt from file."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def respond(message: str, context: Optional[dict] = None) -> str:
    """Simple response placeholder for Emem."""
    return "Emem response placeholder"

def expectation_by_identity(identity: str) -> str:
    """Dynamic expectations based on 24-week gamified identity."""
    senior_roles = ["Strategist", "Director", "Commander", "Chief", "Manager", "Expert", "Lead"]
    mid_roles = ["Analyst", "Associate", "Marketer", "Defender", "Operator"]

    if any(role in identity for role in senior_roles):
        return (
            "This user is at the Executive/Senior level. Expect flawless execution, "
            "strategic thinking, and zero hand-holding. Be extremely demanding."
        )
    elif any(role in identity for role in mid_roles):
        return (
            "This user is at the Intermediate level. Expect solid professional competence "
            "and independence. They should not be making rookie mistakes."
        )
    
    return (
        "This user is at the Intern/Foundational level. They are still ramping up. "
        "Be explicit about what is required and monitor progress strictly."
    )

async def assign_task(
    task_title: str,
    task_brief: str,
    deadline: str,
    client_constraints: Optional[str],
    model: genai.GenerativeModel
) -> str:
    """
    Generate Emem's task assignment message.
    """
    system_prompt = get_system_prompt()

    prompt = f"""
{system_prompt}

---

**TASK TO ASSIGN:**
Title: {task_title}
Brief: {task_brief}
Deadline: {deadline}
Client Constraints: {client_constraints or "None specified"}

Generate a short, sharp task assignment message.
Be direct and set clear expectations.
"""

    response = await model.generate_content_async(prompt)
    return response.text

async def respond_to_message(
    message: str,
    context: dict,
    chat_history: List[dict],
    model: genai.GenerativeModel
) -> str:
    """
    Respond to a deadline/task-related message as Emem.
    """
    bio_summary = context.get("bio_summary")
    current_identity = context.get("current_identity", "Intern")
    expectation_guidance = expectation_by_identity(current_identity)

    system_prompt = get_system_prompt()

    # Recent chat (last 5 messages)
    history_text = ""
    for msg in chat_history[-5:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        history_text += f"{role.upper()}: {content}\n"

    current_task = context.get("task_brief", "No active task")
    deadline = context.get("deadline", "Not set")

    prompt = f"""
{system_prompt}

---

**INTERN PROFILE (FOR CONTEXT ONLY):**
Current Identity/Rank: {current_identity}
Background Summary: {bio_summary or "No background summary available."}

**INTERN CONTEXT (DO NOT MENTION DIRECTLY):**
Expectation Guidance: {expectation_guidance}

**WORK CONTEXT:**
Current Task: {current_task}
Deadline: {deadline}

**RECENT CHAT:**
{history_text}

**USER MESSAGE:**
{message}

Respond as Emem.
- Be brief and directive
- Set expectations appropriate to the intern's current rank/identity
- Reference their background only when it helps clarify expectations
- Do NOT teach or explain how to do the task
"""

    response = await model.generate_content_async(prompt)
    return response.text

async def generate_client_interruption(
    current_task: str,
    interruption_type: str,
    model: genai.GenerativeModel
) -> str:
    """
    Generate a realistic client interruption message to add chaos.
    """
    system_prompt = get_system_prompt()

    interruption_prompts = {
        "scope_change": "The client just emailed asking to change the scope of the project.",
        "constraint_added": "Legal just flagged a compliance issue. We need to add constraints.",
        "urgent_pivot": "Drop everything. The client needs something else urgently.",
        "data_correction": "The data we sent was wrong. The user needs to redo part of the work."
    }

    prompt = f"""
{system_prompt}

---

**CURRENT TASK:** {current_task}

**SITUATION:** {interruption_prompts.get(interruption_type, interruption_prompts['scope_change'])}

Generate a realistic, urgent message from Emem about this change.
Be specific about what needs to change.
This should feel like real workplace chaos — frustrating but professional.
"""

    response = await model.generate_content_async(prompt)
    return response.text

async def generate_video_brief_script(
    task_title: str,
    task_brief: str,
    model: genai.GenerativeModel
) -> str:
    prompt = f"""
        You are Emem, a Nigerian project manager.

        Write a short spoken-style briefing (max 120 words)
        explaining this task to an intern.

        TASK TITLE:
        {task_title}

        TASK BRIEF:
        {task_brief}

        Tone:
        - Clear
        - Direct
        - Encouraging
        - Sounds like a voice note or video explanation
        """

    response = await model.generate_content_async(prompt)
    return response.text.strip()