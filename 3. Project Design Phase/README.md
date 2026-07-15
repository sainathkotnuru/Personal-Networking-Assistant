# 3. Project Design Phase

## Architecture Overview
The solution uses a modular Python architecture with:
- Streamlit frontend for interaction
- FastAPI backend for API endpoints
- Service layer for analysis, generation, history, and feedback
- Pydantic schemas for request and response contracts
- JSON-based local storage

## Design Goals
- Keep the project beginner-friendly
- Separate frontend, API, and business logic
- Enable local and deployed usage with minimal friction
