"""
WDC Labs AI Orchestrator
The Central Brain that routes messages to the appropriate agent.
"""
from typing import Optional, List
import google.generativeai as genai

from .schemas import AgentName, ChatContext, ChatResponse
from .agents import tolu, emem, sola, kemi, recommender


class Orchestrator:
    """
    Central message router enforcing Golden Master routing rules.
    """

    def __init__(self, model: genai.GenerativeModel):
        self.model = model

        self.router_prompt = """You are an intelligent message router for a virtual office training system.

AGENTS:
- Tolu (Onboarding / HR / Admin / Policies / Certificates / Recommendations)
- Emem (Project Manager: tasks, deadlines, briefs, deliverables, clients)
- Sola (Technical Supervisor: code, debugging, reviews, submissions)
- Kemi (Career Coach: CVs, interviews, confidence, emotional support)

ROUTING RULES (STRICT):
1. Work submissions or reviews → Sola
2. Emotional support, CV, interview prep → Kemi
3. Tasks, deadlines, briefs → Emem
4. HR, admin, certificates, recommendations → Tolu
5. Technical help → Sola
6. Default → Sola

Respond with ONLY one word:
Tolu, Emem, Sola, or Kemi
"""

    # ---------------------------
    # AGENT DETERMINATION
    # ---------------------------

    async def determine_agent(self, message: str, context: ChatContext) -> AgentName:
        msg = message.lower()

        # HARD RULES (NO AI)
        if context.is_submission:
            return AgentName.SOLA

        if context.is_first_login:
            return AgentName.TOLU

        if any(k in msg for k in [
            "recommendation letter",
            "reference letter",
            "referee",
            "12 weeks recommendation",
            "24 weeks recommendation"
        ]):
            return AgentName.RECOMMENDER

        # AI ROUTING
        try:
            context_info = f"""
User Level: {context.user_level or 'Unknown'}
Track: {context.track or 'Unknown'}
Task: {context.task_brief or 'None'}
"""

            prompt = f"""{self.router_prompt}

CONTEXT:
{context_info}

USER MESSAGE:
{message}
"""

            response = await self.model.generate_content_async(prompt)
            agent_raw = response.text.strip().title()

            agent_map = {
                "Tolu": AgentName.TOLU,
                "Emem": AgentName.EMEM,
                "Sola": AgentName.SOLA,
                "Kemi": AgentName.KEMI,
            }

            return agent_map.get(agent_raw, AgentName.SOLA)

        except (ValueError, KeyError, AttributeError) as e:
            print(f"[ORCHESTRATOR] AI routing failed: {e}")
            return self._fallback_routing(msg)

    def _fallback_routing(self, msg: str) -> AgentName:
        if any(w in msg for w in ["worried", "scared", "resume", "cv", "interview"]):
            return AgentName.KEMI
        if any(w in msg for w in ["deadline", "brief", "client", "task"]):
            return AgentName.EMEM
        if any(w in msg for w in ["salary", "contract", "policy", "certificate"]):
            return AgentName.TOLU
        return AgentName.SOLA

    # ---------------------------
    # MESSAGE ROUTING
    # ---------------------------

    async def route_message(
        self,
        message: str,
        context: ChatContext,
        chat_history: Optional[List[dict]] = None
    ) -> ChatResponse:

        chat_history = chat_history or []
        agent = await self.determine_agent(message, context)

        ctx = {
            "user_level": context.user_level,
            "track": context.track,
            "task_brief": context.task_brief,
            "deadline": context.deadline,
            "task_id": context.task_id,
            "cv_text": context.cv_text,
            "bio_summary": context.bio_summary,
        }

        if agent == AgentName.TOLU:
            text = await tolu.respond_to_message(message, ctx, chat_history, self.model)

        elif agent == AgentName.EMEM:
            text = await emem.respond_to_message(message, ctx, chat_history, self.model)

        elif agent == AgentName.SOLA:
            text = await sola.respond_to_message(message, ctx, chat_history, self.model)

        elif agent == AgentName.KEMI:
            text = await kemi.respond_to_message(message, ctx, chat_history, self.model)

        elif agent == AgentName.RECOMMENDER:
            result = await recommender.generate_letter(
                cv_text=context.cv_text or "",
                internship_duration_weeks=context.internship_duration_weeks or 12,
                track=context.track or "Unknown",
                performance_summary=context.performance_summary,
                model=self.model
            )
            text = result.get("letter_text", "")

        else:
            text = "I'm not sure how to help with that."

        return ChatResponse(agent=agent, message=text, metadata={"context": ctx})

    # ---------------------------
    # DIRECT ROUTES
    # ---------------------------

    async def assess_bio(self, bio_text: str, track: str) -> dict:
        return await tolu.assess_bio(bio_text, track, self.model)

    async def review_submission(
        self,
        task_title: str,
        task_brief: str,
        submission_content: str,
        client_constraints: Optional[str] = None
    ) -> dict:

        review = await sola.review_submission(
            task_title,
            task_brief,
            submission_content,
            client_constraints,
            self.model
        )

        if review.get("passed"):
            review["portfolio_bullet"] = await kemi.translate_to_cv_bullet(
                task_title,
                task_brief,
                submission_content,
                self.model
            )

        return review

    async def generate_client_interruption(
        self,
        current_task: str,
        interruption_type: str = "scope_change"
    ) -> str:
        return await emem.generate_client_interruption(
            current_task,
            interruption_type,
            self.model
        )

    async def interrogate_submission(
        self,
        submission_content: str,
        approach_used: str
    ) -> str:
        return await sola.interrogate_submission(
            submission_content,
            approach_used,
            self.model
        )

    async def get_soft_skills_feedback(self, recent_interactions: List[dict]) -> str:
        return await kemi.provide_soft_skills_feedback(
            recent_interactions,
            self.model
        )

    async def conduct_mock_interview(
        self,
        interview_type: str,
        question_number: int,
        previous_answer: Optional[str] = None
    ) -> dict:
        return await kemi.conduct_mock_interview(
            interview_type,
            question_number,
            previous_answer,
            self.model
        )

    async def generate_recommendation_letter(
        self,
        cv_text: str,
        internship_duration_weeks: int,
        track: str,
        performance_summary: Optional[str] = None
    ) -> dict:
        return await recommender.generate_letter(
            cv_text,
            internship_duration_weeks,
            track,
            performance_summary,
            self.model
        )
