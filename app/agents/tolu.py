import google.generativeai as genai
from pathlib import Path
from typing import Optional, List
import os

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

**CURRENT TASK: Assess this new intern's background.**

Track they are joining: {track}

Their submitted bio/resume:
\"\"\"
{bio_text}
\"\"\"

Based on this, determine their level and respond with:
1. A brief welcome message (2-3 sentences max)
2. Their assessed level (Level 0, Level 1, or Level 2)
3. Your reasoning (1-2 sentences)

Format your response as JSON:
{{
    "response_text": "Your welcome message here",
    "assessed_level": "Level 0" | "Level 1" | "Level 2",
    "reasoning": "Why you chose this level"
}}
"""

    response = await model.generate_content_async(assessment_prompt)
    
    # Parse JSON from response
    import json
    try:
        # Try to extract JSON from the response
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        result = json.loads(text.strip())
        
        # Set warmup mode for Level 0
        result["warmup_mode"] = result.get("assessed_level") == "Level 0"
        
        return result
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "response_text": response.text,
            "assessed_level": "Level 1",
            "reasoning": "Unable to parse assessment, defaulting to Level 1",
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
    for msg in chat_history[-5:]:  # Last 5 messages for context
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

Respond as Tolu. Be brief and professional.
"""

    response = await model.generate_content_async(prompt)
    return response.text
