# System Architecture

## Components
- Streamlit frontend
- FastAPI backend
- Service layer
- Pydantic models
- JSON storage

## Design Flow
1. User enters event details in Streamlit UI.
2. Backend analyzes the text and extracts themes.
3. Conversation content is generated from the themes.
4. Results are shown in the UI.
5. History and feedback are stored locally.
