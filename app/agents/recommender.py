import google.generativeai as genai
from pathlib import Path
from typing import Optional

# Load prompt from file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "recommender.txt"


def get_system_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


async def generate_letter(
    cv_text: str,
    internship_duration_weeks: int,
    track: str,
    performance_summary: Optional[str],
    model: genai.GenerativeModel
) -> dict:
    """
    Generate a formal recommendation letter for an intern.
    """
    system_prompt = get_system_prompt()

    duration_label = (
        "12-week internship"
        if internship_duration_weeks == 12
        else "24-week internship"
    )

    prompt = f"""
{system_prompt}

---

**INTERNSHIP DETAILS**
Track: {track}
Duration: {duration_label}

**CURRICULUM VITAE**
\"\"\"
{cv_text}
\"\"\"

**PERFORMANCE SUMMARY**
\"\"\"
{performance_summary or "No additional performance summary was provided."}
\"\"\"

Write the recommendation letter now.
"""

    response = await model.generate_content_async(prompt)

    return {
        "letter_text": response.text.strip(),
        "duration_weeks": internship_duration_weeks,
        "tone": "formal"
    }
