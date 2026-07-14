import logging
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models.schemas import (
    ConversationRequest,
    ConversationResponse,
    EventAnalysisRequest,
    EventAnalysisResponse,
    FactCheckRequest,
    FactCheckResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    HistoryItem,
)
from app.services.event_analyzer import EventAnalyzer
from app.services.fact_checker import FactChecker
from app.services.feedback_manager import FeedbackManager
from app.services.history_manager import HistoryManager
from app.services.topic_generator import TopicGenerator


app = FastAPI(title="Personalized Networking Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

analyzer = EventAnalyzer()
generator = TopicGenerator()
checker = FactChecker()
history_manager = HistoryManager()
feedback_manager = FeedbackManager()


@app.get("/", response_model=HealthResponse)
def root() -> HealthResponse:
    """Health check endpoint for the API."""
    logging.info("Received health check request")
    return HealthResponse()


@app.post("/analyze-event", response_model=EventAnalysisResponse)
def analyze_event(request: EventAnalysisRequest) -> EventAnalysisResponse:
    """Analyze event description and extract themes."""
    logging.info("Analyzing event: %s", request.event_name)
    themes = analyzer.extract_themes(request.description)
    return EventAnalysisResponse(event_name=request.event_name, themes=themes)


@app.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation(request: ConversationRequest) -> ConversationResponse:
    """Generate conversation starters and suggestions."""
    logging.info("Generating conversation for event: %s", request.event_name)
    if not request.themes:
        raise HTTPException(status_code=400, detail="At least one theme is required to generate conversation starters.")

    starters = generator.generate_conversation_starters(request.themes)
    follow_up_questions = generator.generate_follow_up_questions(request.themes)
    suggestions = generator.generate_networking_suggestions(request.themes)

    prompt_text = " | ".join(starters)
    history_manager.save_history(request.event_name, prompt_text)

    return ConversationResponse(
        event_name=request.event_name,
        themes=request.themes,
        starters=starters,
        follow_up_questions=follow_up_questions,
        suggestions=suggestions,
    )


@app.post("/fact-check", response_model=FactCheckResponse)
def fact_check(request: FactCheckRequest) -> FactCheckResponse:
    """Verify a topic using Wikipedia API."""
    logging.info("Fact checking topic: %s", request.topic)
    result = checker.verify_topic(request.topic)
    return FactCheckResponse(**result)


@app.get("/history", response_model=List[HistoryItem])
def get_history() -> List[HistoryItem]:
    """Return stored conversation history."""
    raw_history = history_manager.load_history()
    parsed_history = [
        HistoryItem(
            history_id=item["history_id"],
            conversation_id=item["conversation_id"],
            event_name=item["event_name"],
            generated_prompt=item["generated_prompt"],
            date=datetime.fromisoformat(item["date"].replace("Z", "")),
        )
        for item in raw_history
    ]
    return parsed_history


@app.post("/feedback", response_model=FeedbackResponse)
def post_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """Store user feedback for a conversation."""
    logging.info("Storing feedback for conversation: %s", request.conversation_id)
    saved = feedback_manager.store_feedback(request.conversation_id, request.rating, request.comment)
    return FeedbackResponse(**saved)
