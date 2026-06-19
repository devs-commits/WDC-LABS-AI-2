import google.generativeai as genai
from pathlib import Path
from typing import Optional, List
from app.archives.index import ARCHIVE_LIBRARY
import json
import re

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
    Implements STRICT Grading (0-100), 3-strike daily rule, formatting, and holds the 50% passing line.
    """
    system_prompt = get_system_prompt()
    
    # Expand truncation drastically for Gemini 1.5 Pro to ingest full documents
    submission_preview = submission_content[:15000] if len(submission_content) > 15000 else submission_content
    
    # ==========================================
    # 🔥 BULLETPROOF FAIL-SAFE FALLBACK
    # ==========================================
    fallback_result = {
        "feedback": "We experienced a system interruption while reviewing your work. Please double-check your submission and try again.",
        "passed": False,
        "score": 0,
        "error_tag": "[ERR_SYSTEM]"
    }
    
    # ==========================================
    # EVALUATION RULES (FORMATTING & 3-STRIKE)
    # ==========================================
    if attempt_number >= 3:
        attempt_context = """
        🚨 CRITICAL RULE: This is the user's 3rd and FINAL attempt for the day. 
        You must be definitive. Grade them strictly based on the rubric and assign a FINAL SCORE (0-100) regardless of whether they pass or fail.
        
        FORMATTING RULES:
        1. You MUST start your feedback with a large markdown header showing the score: "### 🎯 FINAL SCORE FOR TODAY: [Score]/100\n\n"
        2. If they score below 50, your feedback MUST end with this exact phrase on a new line: "**This was your final attempt for today. Please review my feedback carefully, study the resources, and come back tomorrow to try again.**"
        """
    else:
        attempts_left = 3 - attempt_number
        attempt_context = f"""
        ITERATIVE COACHING MODE (Attempt {attempt_number} of 3 for today).
        The user has {attempts_left} attempt(s) remaining today.
        
        If they pass (50+):
        1. You MUST start your feedback with a large markdown header: "### 🎉 FINAL SCORE: [Score]/100\n\n"
        2. Congratulate them and give structured feedback.
        
        If they fail (<50):
        1. DO NOT give them a "final score" or mention a "0" in your feedback text. 
        2. Start directly with an encouraging header: "### ⚠️ Revisions Needed\n\n"
        3. Point out specific errors cleanly. End by explicitly telling them they have {attempts_left} attempt(s) left today.
        """

    evaluation_rules = f"""
    STRICT WORKPLACE GRADING MODE
    
    You are Sola, the Technical Lead. Evaluate the submission strictly against the brief and client constraints based on their rank: {current_identity}.
    
    {attempt_context}
    
    GRADING RUBRIC & TIERS:
    Assess technical accuracy, business logic, and presentation.
    - 0 to 49 (Failed / Needs Revision): Rejected. Missing core requirements, poor logic, or major errors.
    - 50 to 69 (Pass): Meets bare minimum workplace standards.
    - 70 to 84 (Good): Solid, reliable work with minor areas for improvement.
    - 85 to 100 (Excellent): Exceptional, executive-ready output.
    
    VISUAL FORMATTING RULES (MANDATORY):
    - ALWAYS use double line breaks (\\n\\n) between paragraphs so the text is not jampacked.
    - Use bullet points (-) to list out specific issues or positive points.
    - Use **bold text** to highlight key terms.
    
    RULES:
    1. Focus on major blockers; structure feedback exactly as: Positive, Pivot, Why, Badge Verdict, Tag, Encouragement.
    2. Determine the numerical score (0-100).
    3. Set 'passed' to true ONLY if the score is 50 or higher. Set to false if below 50.
    
    Respond ONLY with valid JSON on a single line (no markdown blocks around the JSON):
    {{"feedback": "Your beautifully formatted, spaced-out coaching message", "passed": true_or_false, "score": integer_0_to_100, "error_tag": "[ERR_TAG]"}}
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

        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            if isinstance(result, dict) and "feedback" in result and "passed" in result:
                if "score" not in result:
                    result["score"] = 50
                    
                # ==========================================
                # 🔥 STRICT SCORE-TO-PASS LOGIC (NO FREE PASSES)
                # ==========================================
                if result["score"] < 50:
                    result["passed"] = False
                else:
                    result["passed"] = True
                    
                return result
        
        # Fallback parsing
        result = json.loads(text)
        if isinstance(result, dict) and "feedback" in result and "passed" in result:
            if "score" not in result:
                result["score"] = 50
                
            # ==========================================
            # 🔥 STRICT SCORE-TO-PASS LOGIC (NO FREE PASSES)
            # ==========================================
            if result["score"] < 50:
                result["passed"] = False
            else:
                result["passed"] = True
                
            return result
            
    except Exception as e:
        print(f"[SOLA ERROR] System or parsing failure: {e}")
    
    return fallback_result


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