import os
from datetime import datetime
from typing import List

import requests
import streamlit as st

from app.services.event_analyzer import EventAnalyzer
from app.services.fact_checker import FactChecker
from app.services.feedback_manager import FeedbackManager
from app.services.history_manager import HistoryManager
from app.services.topic_generator import TopicGenerator

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
USE_LOCAL_SERVICES = os.getenv("USE_LOCAL_SERVICES", "true").lower() in {"1", "true", "yes", "on"}

analyzer = EventAnalyzer()
generator = TopicGenerator()
checker = FactChecker()
history_manager = HistoryManager()
feedback_manager = FeedbackManager()


def fetch_history() -> List[dict]:
    if USE_LOCAL_SERVICES:
        return history_manager.load_history()

    response = requests.get(f"{API_BASE_URL}/history", timeout=10)
    if response.status_code == 200:
        return response.json()
    return []


def build_full_report(event_name: str, description: str, themes: List[str], conversation: dict, fact_checks: List[dict]) -> str:
    lines = []
    lines.append("## Event Description")
    lines.append("```")
    lines.append(description.strip())
    lines.append("```")
    lines.append("---")
    lines.append("## Extracted Themes")
    for theme in themes:
        lines.append(f"- {theme}")
    lines.append("---")
    lines.append("## Generated Conversation Starters")
    starters = conversation.get("starters", [])
    for idx, item in enumerate(starters, start=1):
        lines.append(f"{idx}. {item}")
    lines.append("---")
    lines.append("## Suggested Follow-up Questions")
    for item in conversation.get("follow_up_questions", []):
        lines.append(f"• {item}")
    lines.append("---")
    lines.append("## Networking Suggestions")
    for item in conversation.get("suggestions", []):
        lines.append(f"• {item}")
    lines.append("---")
    lines.append("## Wikipedia Fact Check")
    for result in fact_checks:
        topic = result.get("topic", "")
        status = result.get("status", "")
        summary = result.get("summary", "")
        lines.append(f"{topic}")
        mark = "✓" if status == "verified" else "✗"
        lines.append(f"{mark} {summary}")
        lines.append("")
    lines.append("---")
    lines.append("## Conversation History")
    lines.append("```")
    lines.append(f"Date: {datetime.utcnow().strftime('%d-%m-%Y')}")
    lines.append(f"Event: {event_name}")
    lines.append("\nThemes:")
    for theme in themes:
        lines.append(theme)
    lines.append("\nStatus:")
    lines.append("Saved Successfully")
    lines.append("```")
    return "\n".join(lines)


def analyze_event(event_name: str, description: str) -> dict:
    if USE_LOCAL_SERVICES:
        return {"event_name": event_name, "themes": analyzer.extract_themes(description)}

    payload = {"event_name": event_name, "description": description}
    response = requests.post(f"{API_BASE_URL}/analyze-event", json=payload, timeout=10)
    return response.json() if response.status_code == 200 else {"themes": []}


def generate_conversation(event_name: str, themes: List[str]) -> dict:
    if USE_LOCAL_SERVICES:
        return {
            "event_name": event_name,
            "themes": themes,
            "starters": generator.generate_conversation_starters(themes),
            "follow_up_questions": generator.generate_follow_up_questions(themes),
            "suggestions": generator.generate_networking_suggestions(themes),
        }

    payload = {"event_name": event_name, "themes": themes}
    response = requests.post(f"{API_BASE_URL}/generate-conversation", json=payload, timeout=10)
    return response.json() if response.status_code == 200 else {}


def fact_check(topic: str) -> dict:
    if USE_LOCAL_SERVICES:
        return checker.verify_topic(topic)

    payload = {"topic": topic}
    response = requests.post(f"{API_BASE_URL}/fact-check", json=payload, timeout=10)
    return response.json() if response.status_code == 200 else {}


def fact_check_themes(themes: List[str]) -> List[dict]:
    return [fact_check(theme) for theme in themes]


def submit_feedback(conversation_id: str, rating: int, comment: str) -> dict:
    if USE_LOCAL_SERVICES:
        return feedback_manager.store_feedback(conversation_id, rating, comment)

    payload = {"conversation_id": conversation_id, "rating": rating, "comment": comment}
    response = requests.post(f"{API_BASE_URL}/feedback", json=payload, timeout=10)
    return response.json() if response.status_code == 200 else {}


def main() -> None:
    st.set_page_config(page_title="Personalized Networking Assistant", layout="wide")
    st.sidebar.title("Personalized Networking Assistant")
    menu = st.sidebar.radio("Navigation", ["Home", "History", "Feedback"])

    if menu == "Home":
        st.title("AI Conversation Starter Generator")
        st.write(
            "Enter your event description to extract themes, generate tailored conversation starters, and verify facts with Wikipedia."
        )

        event_name = st.text_input("Event Name", "Networking Mixer")
        description = st.text_area("Event Description", height=200)

        analysis = {}
        if st.button("Analyze Event"):
            if not event_name or not description:
                st.warning("Please provide both an event name and description.")
            else:
                analysis = analyze_event(event_name, description)
                st.session_state["analysis"] = analysis

        if "analysis" in st.session_state:
            analysis = st.session_state["analysis"]

        themes = analysis.get("themes", [])
        if themes:
            st.success("Themes extracted successfully.")
            st.markdown("## Event Description")
            st.code(description or "", language="text")
            st.markdown("---")
            st.markdown("## Extracted Themes")
            for theme in themes:
                st.write(f"- {theme}")

        if themes:
            st.markdown("---")
            st.markdown("## Generated Conversation Starters")
            if st.button("Generate Conversation Starters"):
                conversation = generate_conversation(event_name, themes)
                fact_checks = [fact_check(theme) for theme in themes]
                report = build_full_report(event_name, description, themes, conversation, fact_checks)
                st.session_state["conversation"] = conversation
                st.session_state["fact_checks"] = fact_checks
                st.session_state["report"] = report

        if "conversation" in st.session_state:
            conversation = st.session_state["conversation"]
            starters = conversation.get("starters", [])
            follow_up = conversation.get("follow_up_questions", [])
            suggestions = conversation.get("suggestions", [])

            if starters:
                st.markdown("### Conversation Starters")
                for idx, item in enumerate(starters, start=1):
                    st.write(f"{idx}. {item}")

            if follow_up:
                st.markdown("### Suggested Follow-up Questions")
                for item in follow_up:
                    st.write(f"• {item}")

            if suggestions:
                st.markdown("### Networking Suggestions")
                for item in suggestions:
                    st.write(f"• {item}")

            st.success("Generated conversation content successfully.")

            st.markdown("---")
            st.markdown("## Conversation History")
            st.write(f"**Event:** {event_name}")
            st.write(f"**Status:** Saved Successfully")

        if "report" in st.session_state:
            st.markdown("---")
            st.markdown("## Full Report")
            st.code(st.session_state["report"], language="markdown")

        st.markdown("---")
        st.markdown("## Wikipedia Fact Check")
        topic = st.text_input("Topic to verify", ", ".join(themes) if themes else "Artificial Intelligence")
        if st.button("Verify Topic", key="verify_topic"):
            fact_result = fact_check(topic)
            status = fact_result.get("status", "error")
            st.write(f"**Topic:** {fact_result.get('topic', '')}")
            st.write(f"**Status:** {status}")
            st.write(fact_result.get("summary", "No summary available."))

        if "fact_checks" in st.session_state:
            st.markdown("---")
            st.markdown("### Automatic Theme Fact Checks")
            for result in st.session_state["fact_checks"]:
                mark = "✓" if result.get("status") == "verified" else "✗"
                st.write(f"**{result.get('topic')}** — {mark}")
                st.write(result.get("summary", "No summary available."))
                st.write("")

    elif menu == "History":
        st.title("Conversation History")
        history = fetch_history()
        if history:
            for item in history:
                st.markdown(f"**{item.get('event_name')}** — {item.get('date')}")
                st.write(item.get("generated_prompt"))
                st.write("---")
        else:
            st.info("No conversation history has been saved yet.")

    elif menu == "Feedback":
        st.title("Submit Feedback")
        st.write("Provide feedback after trying a generated conversation starter.")

        conversation_id = st.text_input("Conversation ID")
        rating = st.slider("Rating", min_value=1, max_value=5, value=4)
        comment = st.text_area("Comment", height=120)

        if st.button("Send Feedback"):
            if not conversation_id:
                st.warning("A conversation ID is required to store feedback.")
            else:
                response = submit_feedback(conversation_id, rating, comment)
                if response:
                    st.success("Feedback submitted successfully.")
                    st.write(response)
                else:
                    st.error("Could not submit feedback at this time.")

    st.sidebar.write("---")
    st.sidebar.write("Built with FastAPI, Streamlit, DistilBERT, GPT-2, and Wikipedia.")


if __name__ == "__main__":
    main()
