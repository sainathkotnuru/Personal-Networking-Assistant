from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class EventAnalysisRequest(BaseModel):
    event_name: str = Field(...)
    description: str = Field(...)


class EventAnalysisResponse(BaseModel):
    event_name: str
    themes: List[str]


class ConversationRequest(BaseModel):
    event_name: str = Field(...)
    themes: List[str]


class ConversationResponse(BaseModel):
    event_name: str
    themes: List[str]
    starters: List[str]
    follow_up_questions: List[str]
    suggestions: List[str]


class FactCheckRequest(BaseModel):
    topic: str = Field(...)


class FactCheckResponse(BaseModel):
    topic: str
    summary: str
    status: str


class FeedbackRequest(BaseModel):
    conversation_id: str = Field(...)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None)


class FeedbackResponse(BaseModel):
    feedback_id: str
    conversation_id: str
    rating: int
    comment: Optional[str]


class HistoryItem(BaseModel):
    history_id: str
    conversation_id: str
    event_name: str
    generated_prompt: str
    date: datetime


class HealthResponse(BaseModel):
    status: str = "ok"
    message: str = "Personalized Networking Assistant is running."
