"""
WDC Labs AI Orchestrator
The Central Brain that routes messages to the appropriate agent.
"""
from typing import Optional, List
import google.generativeai as genai

from .schemas import AgentName, ChatContext, ChatResponse
from .agents import tolu, emem, sola, kemi, recommender
from .utils.link_verifier import clean_broken_links


class Orchestrator:
    """
    Central message router enforcing Golden Master routing rules.
    """

    def __init__(self, model: genai.GenerativeModel):
        self.model = model

        self.router_prompt = """You are an intelligent message categorizer for a virtual office training system.

Your job is to DETECT the category of the user's message and respond with ONLY the agent name.

AGENT CATEGORIES:

**TOLU** (Onboarding Officer) - Handles:
- Initial setup, CV/bio assessment
- HR policies, contracts, salary questions
- Certificate requests, program info
- Recommendation letters

**EMEM** (Project Manager) - Handles:
- Task assignments and briefs
- Deadlines, deliverables, scope
- Client requirements and constraints
- Project changes or interruptions
- Work planning questions

**SOLA** (Technical Supervisor) - Handles:
- Code reviews, debugging help
- Technical problem-solving
- Work submissions and feedback
- Technical error explanation

**KEMI** (Career Coach) - Handles:
- CV/resume feedback
- Interview preparation
- Career advice, confidence building
- Emotional support, struggle handling
- Portfolio translation

DETECTION LOGIC (in priority order):
1. If message contains submission → Sola
2. If message shows emotional struggle, fear, confidence issue → Kemi
3. If message asks about CV, interview, career → Kemi
4. If message mentions task, deadline, project scope → Emem
5. If message asks for technical help, debugging → Sola
6. If message about HR, admin, policies → Tolu
7. Default → Sola

OUTPUT FORMAT:
Respond with ONLY one word agent name - no explanation:
Tolu
or
Emem
or
Sola
or
Kemi
"""

    # ---------------------------
    # AGENT DETERMINATION
    # ---------------------------

    async def determine_agent(self, message: str, context: ChatContext) -> AgentName:
        msg = message.lower()

        # HARD RULES (NO AI NEEDED - CERTAINTY)
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

        # AI-POWERED CATEGORY DETECTION
        try:
            # return AgentName.SOLA  # temporary
            context_info = f"""
User Level: {context.user_level or 'Unknown'}
Track: {context.track or 'Unknown'}
Active Task: {context.task_brief or 'None'}
"""

            prompt = f"""{self.router_prompt}

CONTEXT:
{context_info}

USER MESSAGE:
{message}

Detect the appropriate agent category and respond with ONLY the agent name.
"""

            response = await self.model.generate_content_async(prompt)
            agent_raw = response.text.strip().title()

            agent_map = {
                "Tolu": AgentName.TOLU,
                "Emem": AgentName.EMEM,
                "Sola": AgentName.SOLA,
                "Kemi": AgentName.KEMI,
            }

            detected_agent = agent_map.get(agent_raw, None)
            
            # If AI detection failed, use fallback
            if detected_agent is None:
                print(f"[ORCHESTRATOR] AI detection unclear: '{agent_raw}' - using fallback")
                return self._fallback_routing(msg)
            
            return detected_agent

        except Exception as e:
            print(f"[ORCHESTRATOR] AI detection failed: {e} - using fallback")
            return self._fallback_routing(msg)

    def _fallback_routing(self, msg: str) -> AgentName:
        """Fallback routing using heuristic rules (safe & reliable)"""
        
        # Emotional/Career support keywords
        emotional_keywords = ["worried", "scared", "help", "struggle", "stuck", "confused", "lost", "scared", "anxious", "stressed"]
        career_keywords = ["resume", "cv", "interview", "portfolio", "career", "confidence", "skill", "growth", "job"]
        
        # Task/Project keywords
        task_keywords = ["deadline", "brief", "task", "project", "client", "deliverable", "submit", "due", "when"]
        
        # Technical keywords
        tech_keywords = ["code", "debug", "error", "bug", "function", "variable", "syntax", "python", "javascript", "fix"]
        
        # HR/Admin keywords
        hr_keywords = ["salary", "contract", "policy", "certificate", "certificate", "onboarding", "admin", "hours", "leave"]
        
        # Count keyword matches
        emotional_count = sum(1 for k in emotional_keywords if k in msg)
        career_count = sum(1 for k in career_keywords if k in msg)
        task_count = sum(1 for k in task_keywords if k in msg)
        tech_count = sum(1 for k in tech_keywords if k in msg)
        hr_count = sum(1 for k in hr_keywords if k in msg)
        
        # Route based on highest score
        scores = {
            AgentName.KEMI: emotional_count + career_count,
            AgentName.EMEM: task_count,
            AgentName.SOLA: tech_count,
            AgentName.TOLU: hr_count
        }
        
        best_agent = max(scores, key=scores.get)
        
        # If no clear winner, default to Sola (technical)
        if all(v == 0 for v in scores.values()):
            return AgentName.SOLA
        
        return best_agent

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

        # Clean any broken links from the response
        from app.utils.link_verifier import clean_broken_links_sync
        text = clean_broken_links_sync(text)

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
