from pydantic import BaseModel
from typing import Optional, List, Literal
from enum import Enum


class AgentName(str, Enum):
    TOLU = "Tolu"
    EMEM = "Emem"
    SOLA = "Sola"
    KEMI = "Kemi"


class UserLevel(str, Enum):
    LEVEL_0 = "Level 0"
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"


# Chat Request/Response
class ChatContext(BaseModel):
    task_id: Optional[str] = None
    is_submission: bool = False
    is_first_login: bool = False
    user_level: Optional[str] = None
    track: Optional[str] = None
    task_brief: Optional[str] = None
    deadline: Optional[str] = None


class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: ChatContext = ChatContext()
    chat_history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    agent: AgentName
    message: str
    metadata: Optional[dict] = None


# Bio/Resume Assessment
class BioAssessmentRequest(BaseModel):
    user_id: str
    bio_text: Optional[str] = None
    file_url: Optional[str] = None
    track: str


class BioAssessmentResponse(BaseModel):
    response_text: str
    assessed_level: UserLevel
    reasoning: str
    warmup_mode: bool = False


# Task Generation
class TaskGenerationRequest(BaseModel):
    user_id: str
    track: str
    experience_level: str
    task_number: int = 1
    previous_task_performance: Optional[str] = None
    user_city: Optional[str] = None
    user_country: Optional[str] = None


class GeneratedTask(BaseModel):
    title: str
    brief_content: str
    difficulty: str
    client_constraints: Optional[str] = None
    attachments: Optional[List[str]] = []
    ai_persona_config: Optional[dict] = None


class TaskGenerationResponse(BaseModel):
    tasks: List[GeneratedTask]


# Work Submission Review
class SubmissionReviewRequest(BaseModel):
    user_id: str
    task_id: str
    file_url: Optional[str] = None
    file_content: Optional[str] = None
    task_title: str
    task_brief: str
    chat_history: Optional[List[dict]] = []


class SubmissionReviewResponse(BaseModel):
    agent: Literal["Sola"] = "Sola"
    feedback: str
    passed: bool
    score: Optional[int] = None
    portfolio_bullet: Optional[str] = None  # Kemi's CV translation if passed


# Portfolio Generation
class PortfolioBulletRequest(BaseModel):
    task_title: str
    task_description: str
    user_submission: str


class PortfolioBulletResponse(BaseModel):
    skill_tag: str
    bullet_point: str
