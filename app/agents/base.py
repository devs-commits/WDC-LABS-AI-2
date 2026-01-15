from pathlib import Path
import google.generativeai as genai
from typing import Optional


class BaseAgent:
    def __init__(self, name: str, prompt_file: str, model_name: str = "gemini-1.5-pro"):
        self.name = name
        self.system_prompt = self._load_prompt(prompt_file)

        # Create a per-agent model instance (best-effort)
        try:
            self.model = genai.GenerativeModel(model_name)
        except (AttributeError, TypeError, RuntimeError, ImportError):
            self.model = None

    def _load_prompt(self, prompt_file: str) -> str:
        path = Path(prompt_file)
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_file}")
        return path.read_text(encoding="utf-8")

    async def respond(self, user_message: str, _context: Optional[dict] = None) -> str:
        """Generate a short response using the agent's model.

        If the model isn't available, return an empty string to avoid runtime errors.
        """
        if not self.model:
            return ""

        # Prefer async generation API when available
        try:
            response = await self.model.generate_content_async(user_message)
            return response.text
        except (AttributeError, RuntimeError):
            try:
                resp = self.model.generate_content(user_message)
                return getattr(resp, "text", "")
            except (AttributeError, RuntimeError):
                return ""
