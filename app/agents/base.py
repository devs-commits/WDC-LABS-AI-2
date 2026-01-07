from pathlib import Path
import os
from google import genai

# Configure Gemini once
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class BaseAgent:
    def __init__(self, name: str, prompt_file: str):
        self.name = name
        self.system_prompt = self._load_prompt(prompt_file)

        # One model instance per agent is fine
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=self.system_prompt
        )

    def _load_prompt(self, prompt_file: str) -> str:
        path = Path(prompt_file)
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_file}")
        return path.read_text(encoding="utf-8")

    def respond(self, user_message: str, context: dict | None = None) -> str:
        """
        context is optional and future-proofed (memory, metadata, etc.)
        """

        response = self.model.generate_content(
            user_message,
            generation_config={
                "temperature": 0.3,
            }
        )

        return response.text.strip()
