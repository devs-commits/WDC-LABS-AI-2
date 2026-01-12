# app/intent_classifier.py
from dotenv import load_dotenv
import json
import os
from typing import Dict
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

INTENTS = {
    "hr_onboarding": "tolu",
    "project_manager": "emem",
    "supervisor": "sola",
    "career_strategist": "kemi",
}

INTENT_SYSTEM_PROMPT = """
You are an intent classification engine for a virtual AI office.

Available intents:
- hr_onboarding
- project_manager
- supervisor
- career_strategist

Rules:
- Return ONLY valid JSON
- No markdown
- No extra text

JSON format:
{
  "intent": "<intent>",
  "confidence": <0-1>,
  "reason": "<short>"
}
"""


def classify_intent(message: str) -> str:
    # pylint: disable=unexpected-keyword-arg
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents=[
            {"role": "system", "parts": [INTENT_SYSTEM_PROMPT]},
            {"role": "user", "parts": [message]},
        ],
        generation_config={"temperature": 0.0},
)


    raw = response.text.strip()

    try:
        data: Dict = json.loads(raw)
        intent = data.get("intent")
        if intent in INTENTS:
            return intent
    except json.JSONDecodeError:
        pass

    # HARD fallback
    return "hr_onboarding"
