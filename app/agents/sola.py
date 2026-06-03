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

def respond(message: str, context: Optional[dict] = None) -> str:
    """Simple response placeholder for Sola."""
    return "Sola response placeholder"

def select_task_resources(task_brief: str, track: str) -> list:
    resources = []
    task_lower = task_brief.lower()
    for item in ARCHIVE_LIBRARY.get(track, []):
        if any(tag in task_lower for tag in item["tags"]):
            resources.append(item)
    resources += ARCHIVE_LIBRARY.get("general", [])[:1]
    return resources[:3]


async def review_submission(
    task_title: str,
    task_brief: str,
    submission_content: str,
    client_constraints: Optional[str],
    model: genai.GenerativeModel,
    attempt_number: int = 1,
    current_identity: str = "Intern",
    badge_opportunity: Optional[str] = None
) -> dict:
    """
    Review a user's submission as Sola (Technical Lead).
    Implements the 3-Strike Rule, Final Evaluation Mode, and Badge evaluation.
    """
    system_prompt = get_system_prompt()
    
    # Expand truncation drastically for Gemini 1.5 Pro to ingest full documents
    submission_preview = submission_content[:15000] if len(submission_content) > 15000 else submission_content
    
    # --- 3-TRIAL LIMIT LOGIC ---
    if attempt_number >= 3:
        evaluation_rules = """
        🚨 CRITICAL RULE: This is the user's 3rd and final attempt for the day.
        You MUST NOT ask them to revise or resubmit. 
        You MUST do the following:
        1. Grade the submission as best as you can and assign a final score out of 100.
        2. Set the 'passed' boolean to true (so the system moves them forward).
        3. Provide this exact feedback in your response: "We are moving you to the next stage so you can continue progressing, but please take time to study the materials provided for this task to strengthen your understanding."
        
        Respond ONLY with valid JSON on a single line (no markdown blocks around the JSON):
        {"feedback": "Formatted final evaluation report including the mandatory feedback sentence", "passed": true, "score": integer_0_to_100, "error_tag": "[ERR_GENERAL]"}
        """
    else:
        evaluation_rules = f"""
        ITERATIVE COACHING MODE (Attempt {attempt_number} of 3).
        1. Evaluate based on their rank: {current_identity}. Hold higher ranks to a flawless standard.
        2. Check if submission addresses the task requirements and client constraints.
        3. Check code/analytical quality and professionalism.
        4. Focus on major blockers; structure feedback exactly as: Positive, Pivot, Why, Badge Verdict, Tag, Encouragement.
        
        Respond ONLY with valid JSON on a single line (no markdown blocks around the JSON):
        {{"feedback": "Your detailed 6-part coaching message", "passed": true_or_false, "score": integer_0_to_100, "error_tag": "[ERR_TAG]"}}
        """

    prompt = f"""
{system_prompt}

---

**TASK TO REVIEW:**
Title: {task_title}
Brief: {task_brief}
Client Constraints: {client_constraints or "None specified"}
Attempt Number: {attempt_number}/3
Current Identity: {current_identity}
Badge Opportunity: {badge_opportunity or "None"}

**USER'S SUBMISSION:**
\"\"\"
{submission_preview}
\"\"\"

**REVIEW INSTRUCTIONS:**
{evaluation_rules}
"""

    try:
        response = await model.generate_content_async(prompt)
        text = response.text.strip()
        
        # Clean markdown code blocks from response
        if text.startswith("```"):
            lines = text.split('\n')
            if len(lines) > 1:
                text = '\n'.join(lines[1:])
                if text.endswith("```"):
                    text = text[:-3]

        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            if isinstance(result, dict) and "feedback" in result and "passed" in result:
                if "score" not in result:
                    result["score"] = 50
                return result
        
        # Fallback parsing
        result = json.loads(text)
        if isinstance(result, dict) and "feedback" in result and "passed" in result:
            if "score" not in result:
                result["score"] = 50
            return result
            
    except (json.JSONDecodeError, AttributeError, IndexError) as e:
        print(f"[SOLA ERROR] JSON parsing failed: {e}")
    
    return {
        "feedback": "Unable to generate review due to a system error. Please resubmit your work.",
        "passed": False,
        "score": 0,
        "error_tag": "[ERR_SYSTEM]"
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
    current_identity = context.get("current_identity", "Intern")
    
    prompt = f"""
{system_prompt}

---

**CONTEXT:**
Current Task: {current_task}
Current Identity: {current_identity}

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