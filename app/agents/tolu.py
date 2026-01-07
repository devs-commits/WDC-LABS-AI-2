import google.generativeai as genai
from pathlib import Path
from typing import List
import json

# Load prompt from file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "tolu.txt"


def get_system_prompt() -> str:
    """Load Tolu's system prompt from file."""
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


async def assess_bio(
    bio_text: str,
    track: str,
    model: genai.GenerativeModel
) -> dict:
    """
    Analyze a user's bio/resume and assign their skill level.

    Returns:
        dict with response_text, assessed_level, reasoning, warmup_mode
    """
    system_prompt = get_system_prompt()

    assessment_prompt = f"""
{system_prompt}

---

**TASK: INTERN BACKGROUND REVIEW**

You are reviewing this intern’s submitted bio/resume as part of an intake process.
You are experienced and realistic — not overly encouraging.

Track: {track}

Submitted bio/resume:
\"\"\"
{bio_text}
\"\"\"

Assess the intern based on:
- Evidence of hands-on work (projects, tools, real tasks)
- Clarity and specificity of experience
- Gaps or missing fundamentals
- Signals of readiness vs curiosity-only interest

Then respond in JSON with:

1. A short, professional welcome (neutral tone, not hype)
2. Assessed level:
   - Level 0: New / theory-only / unclear exposure
   - Level 1: Some hands-on exposure, still inconsistent
   - Level 2: Clear practical experience and autonomy
3. Reasoning:
   - Explicitly reference what was present or missing in the bio
   - 1–2 sentences max
   - No motivational language

Format strictly as JSON:
{{
  "response_text": "...",
  "assessed_level": "Level 0 | Level 1 | Level 2",
  "reasoning": "..."
}}
"""

    response = await model.generate_content_async(assessment_prompt)

    try:
        text = response.text.strip()

        # Strip markdown fences if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        result = json.loads(text.strip())

        # Warmup mode only for Level 0
        result["warmup_mode"] = result.get("assessed_level") == "Level 0"

        return result

    except json.JSONDecodeError:
        # Safe fallback
        return {
            "response_text": response.text,
            "assessed_level": "Level 1",
            "reasoning": "Unable to reliably parse assessment; defaulting to Level 1.",
            "warmup_mode": False
        }


async def respond_to_message(
    message: str,
    context: dict,
    chat_history: List[dict],
    model: genai.GenerativeModel
) -> str:
    """
    Respond to an administrative or general message as Tolu.
    """
    system_prompt = get_system_prompt()

    history_text = ""
    for msg in chat_history[-5:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        history_text += f"{role.upper()}: {content}\n"

    prompt = f"""
{system_prompt}

---

**CONTEXT:**
User Level: {context.get('user_level', 'Unknown')}
Track: {context.get('track', 'Unknown')}

**RECENT CHAT:**
{history_text}

**USER MESSAGE:**
{message}

Respond as Tolu.
- Be professional
- Be concise
- No coaching unless explicitly asked
"""

    response = await model.generate_content_async(prompt)
    return response.text
