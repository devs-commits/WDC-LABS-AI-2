import google.generativeai as genai
from pathlib import Path
from typing import Optional, List

# Load prompt from file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "emem.txt"


def get_system_prompt() -> str:
    """Load Emem's system prompt from file."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def respond(message: str, context: dict | None = None) -> str:
    """Simple response placeholder for Emem."""
    return "Emem response placeholder"

def expectation_by_level(level: str) -> str:
    if level == "Level 0":
        return (
            "This intern is still ramping up. Be explicit about what is required. "
            "Do not assume prior experience. Set clear, achievable expectations."
        )

    if level == "Level 2":
        return (
            "This intern has demonstrated strong capability. "
            "Expect ownership, initiative, and minimal hand-holding."
        )

    # Default: Level 1
    return (
        "This intern has some experience but may still need guidance. "
        "Set standard intern expectations and monitor progress."
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

    # Intern background context (derived from CV by another agent)
    bio_summary = context.get("bio_summary")
    user_level = context.get("user_level", "Unknown")
    user_level = context.get("user_level", "Level 1")
    expectation_guidance = expectation_by_level(user_level)

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
Level: {user_level}
Background Summary: {bio_summary or "No background summary available."}

**INTERN CONTEXT (DO NOT MENTION DIRECTLY):**
Intern Level: {user_level}
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
- Set expectations appropriate to the intern's level
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

    interruption_type:
    - 'scope_change'
    - 'constraint_added'
    - 'urgent_pivot'
    - 'data_correction'
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



