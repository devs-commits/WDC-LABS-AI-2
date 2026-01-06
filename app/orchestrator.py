"""
WDC Labs AI Orchestrator
The "Central Brain" that routes messages to the appropriate agent based on context.
"""

import google.generativeai as genai
from typing import Optional, List
from .schemas import AgentName, ChatContext, ChatResponse
from .agents import tolu, emem, sola, kemi


class Orchestrator:
    """
    The Message Router that determines which agent should respond.
    
    Routing Logic:
    - Submission context → Sola (Technical Supervisor)
    - "help", "worried", "resume", "scared" → Kemi (Career Coach)
    - "deadline", "brief", "client", "task" → Emem (Project Manager)
    - First login, "salary", "contract", "hours" → Tolu (Onboarding)
    - Default → Sola (for general technical queries)
    """
    
    def __init__(self, model: genai.GenerativeModel):
        self.model = model
        
        # Agent router prompt for AI-based routing
        self.router_prompt = """You are an intelligent message router for a virtual office training system.
Your job is to determine which AI agent should respond to a user's message.

**AGENTS:**
- **Tolu** (Onboarding Officer): Handles administrative questions, HR topics, contracts, salary, working hours, policies, onboarding, certificates, recommendations.
- **Emem** (Project Manager): Handles deadlines, task assignments, deliverables, client work, project status, priorities, briefs, submissions.
- **Sola** (Technical Supervisor): Handles technical questions, code reviews, debugging, errors, how-to questions, technical explanations, work reviews.
- **Kemi** (Career Coach): Handles emotional support, career advice, interview prep, resume/CV help, encouragement, motivation, feelings of doubt or anxiety.

**ROUTING RULES:**
1. If the user is submitting work for review → Sola
2. If the user mentions feeling worried, stressed, overwhelmed, or needs encouragement → Kemi
3. If the user asks about deadlines, tasks, or project work → Emem
4. If the user asks administrative/HR questions → Tolu
5. If the user has a technical question or needs help with code/work → Sola
6. Default to Sola for general queries

**RESPOND WITH ONLY ONE WORD:** Tolu, Emem, Sola, or Kemi
"""
    
    async def determine_agent(self, message: str, context: ChatContext) -> AgentName:
        """
        Use AI to determine which agent should respond based on message content and context.
        """
        # Priority 1: Submission always goes to Sola
        if context.is_submission:
            return AgentName.SOLA
        
        # Priority 2: First login goes to Tolu
        if context.is_first_login:
            return AgentName.TOLU
        
        # Use AI to determine the best agent
        try:
            context_info = f"""
User Level: {context.user_level or 'Unknown'}
Track: {context.track or 'Unknown'}
Current Task: {context.task_brief or 'None'}
"""
            
            routing_request = f"""{self.router_prompt}

**CONTEXT:**
{context_info}

**USER MESSAGE:**
{message}

Which agent should respond? Reply with ONLY the agent name (Tolu, Emem, Sola, or Kemi):"""

            response = await self.model.generate_content_async(routing_request)
            agent_name = response.text.strip().title()
            
            # Map response to AgentName enum
            agent_map = {
                "Tolu": AgentName.TOLU,
                "Emem": AgentName.EMEM,
                "Sola": AgentName.SOLA,
                "Kemi": AgentName.KEMI
            }
            
            return agent_map.get(agent_name, AgentName.SOLA)
            
        except Exception as e:
            print(f"AI routing failed, using fallback: {e}")
            # Fallback to simple keyword matching
            return self._fallback_routing(message)
    
    def _fallback_routing(self, message: str) -> AgentName:
        """Fallback keyword-based routing if AI fails."""
        lowercase_msg = message.lower()
        
        if any(w in lowercase_msg for w in ['help', 'worried', 'scared', 'career', 'resume', 'cv']):
            return AgentName.KEMI
        if any(w in lowercase_msg for w in ['deadline', 'brief', 'client', 'task', 'submit']):
            return AgentName.EMEM
        if any(w in lowercase_msg for w in ['salary', 'contract', 'hours', 'policy']):
            return AgentName.TOLU
        
        return AgentName.SOLA
    
    async def route_message(
        self,
        message: str,
        context: ChatContext,
        chat_history: List[dict] = []
    ) -> ChatResponse:
        """
        Route the message to the appropriate agent and get response.
        """
        agent = await self.determine_agent(message, context)
        
        # Build context dict for agent functions
        ctx = {
            "user_level": context.user_level,
            "track": context.track,
            "task_brief": context.task_brief,
            "deadline": context.deadline,
            "task_id": context.task_id
        }
        
        # Route to appropriate agent
        if agent == AgentName.TOLU:
            response_text = await tolu.respond_to_message(
                message, ctx, chat_history, self.model
            )
        elif agent == AgentName.EMEM:
            response_text = await emem.respond_to_message(
                message, ctx, chat_history, self.model
            )
        elif agent == AgentName.SOLA:
            response_text = await sola.respond_to_message(
                message, ctx, chat_history, self.model
            )
        elif agent == AgentName.KEMI:
            response_text = await kemi.respond_to_message(
                message, ctx, chat_history, self.model
            )
        else:
            response_text = "I'm not sure how to help with that. Please rephrase your question."
        
        return ChatResponse(
            agent=agent,
            message=response_text,
            metadata={"context": ctx}
        )
    
    async def assess_bio(self, bio_text: str, track: str) -> dict:
        """
        Route bio assessment to Tolu.
        """
        return await tolu.assess_bio(bio_text, track, self.model)
    
    async def review_submission(
        self,
        task_title: str,
        task_brief: str,
        submission_content: str,
        client_constraints: Optional[str] = None
    ) -> dict:
        """
        Route submission review to Sola.
        """
        review_result = await sola.review_submission(
            task_title, task_brief, submission_content, client_constraints, self.model
        )
        
        # If passed, get Kemi to translate to CV bullet
        if review_result.get("passed", False):
            cv_bullet = await kemi.translate_to_cv_bullet(
                task_title, task_brief, submission_content, self.model
            )
            review_result["portfolio_bullet"] = cv_bullet
        
        return review_result
    
    async def generate_client_interruption(
        self,
        current_task: str,
        interruption_type: str = "scope_change"
    ) -> str:
        """
        Generate a realistic mid-task client interruption (the "Moving Target").
        """
        return await emem.generate_client_interruption(
            current_task, interruption_type, self.model
        )
    
    async def interrogate_submission(
        self,
        submission_content: str,
        approach_used: str
    ) -> str:
        """
        Sola's Socratic Defense - interrogate the user's choices.
        """
        return await sola.interrogate_submission(
            submission_content, approach_used, self.model
        )
    
    async def get_soft_skills_feedback(
        self,
        recent_interactions: List[dict]
    ) -> str:
        """
        Get Kemi's soft skills feedback based on recent interactions.
        """
        return await kemi.provide_soft_skills_feedback(
            recent_interactions, self.model
        )
    
    async def conduct_mock_interview(
        self,
        interview_type: str,
        question_number: int,
        previous_answer: Optional[str] = None
    ) -> dict:
        """
        Conduct a mock interview session with Kemi.
        """
        return await kemi.conduct_mock_interview(
            interview_type, question_number, previous_answer, self.model
        )
