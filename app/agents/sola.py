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
    attempt_number: int = 1  # <--- Added attempt tracking
) -> dict:
    """
    Review a user's submission as Sola (Technical Lead).
    Implements the 3-Strike Rule and Final Evaluation Mode.
    """
    system_prompt = get_system_prompt()
    
    # Truncate very long submissions to avoid token limits
    submission_preview = submission_content[:3000] if len(submission_content) > 3000 else submission_content
    
    # --- 3-TRIAL LIMIT LOGIC ---
    if attempt_number >= 3:
        evaluation_rules = """
        🚨 FINAL EVALUATION MODE TRIGGERED (Attempt 3 of 3).
        Stop iterative coaching. Conduct a full end-to-end assessment of the learner’s submission.
        Identify and present ALL remaining issues, weaknesses, inconsistencies, and missing requirements in a single response.
        Do not withhold additional feedback for future revisions.
        Evaluate strictly according to the assignment brief and evidence presented.
        Shift from iterative coaching to comprehensive final assessment.
        
        The 'feedback' string MUST follow this EXACT format using Markdown headers:
        
        ### 1. Overall Evaluation
        [Concise summary of overall quality]
        
        ### 2. Strengths
        [What was done correctly and effectively]
        
        ### 3. Weaknesses
        [All remaining analytical, structural, factual, or methodological issues]
        
        ### 4. Missing, Unsupported, or Incorrect Requirements
        [Explicitly identify missing requirements, unsupported assumptions, or deviations]
        
        ### 5. Recommendations for Improvement
        [Actionable suggestions for professional growth]
        
        ### 6. Final Score
        [Score out of 100%]
        
        Respond ONLY with valid JSON on a single line (no markdown blocks around the JSON):
        {"feedback": "Formatted final evaluation report matching the required structure above", "passed": true_or_false, "score": integer_0_to_100, "improvement_points": ["Point 1", "Point 2"]}
        """
    else:
        evaluation_rules = f"""
        ITERATIVE COACHING MODE (Attempt {attempt_number} of 3).
        1. Check if submission addresses the task requirements.
        2. Check code/analytical quality and professionalism.
        3. Check if client constraints were followed.
        4. Apply the 60% Rejection Rule - reject unless truly excellent.
        5. Focus on major blockers; do not reveal every single micro-flaw if they are overwhelming. Save detailed grading for Attempt 3.
        
        Respond ONLY with valid JSON on a single line (no markdown blocks around the JSON):
        {{"feedback": "Your detailed coaching message", "passed": true_or_false, "score": integer_0_to_100, "improvement_points": ["Point 1"]}}
        """

    prompt = f"""
{system_prompt}

---

**TASK TO REVIEW:**
Title: {task_title}
Brief: {task_brief}
Client Constraints: {client_constraints or "None specified"}
Attempt Number: {attempt_number}/3

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
        "improvement_points": ["System parsing error occurred"]
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