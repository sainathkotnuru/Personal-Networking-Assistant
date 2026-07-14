# Personalized Networking Assistant

## Project Description

The Personalized Networking Assistant is an AI-powered web application that helps users generate intelligent, personalized conversation starters for professional or social networking events.

The application analyzes event descriptions using DistilBERT, extracts important themes, generates context-aware conversation starters with GPT-2, verifies topic facts using the Wikipedia API, and stores conversation history locally in JSON format.

## Features

- Analyze event descriptions and extract themes
- Generate conversation starters, follow-up questions, and networking suggestions
- Verify topics using Wikipedia
- Store conversation history in local JSON files
- Collect user feedback and calculate statistics
- FastAPI backend with Pydantic validation
- Streamlit frontend for a beginner-friendly UI
- Unit tests using pytest

## Installation

1. Clone repo:
   ```bash
   git clone <repo-url>
   cd PersonalizedNetworkingAssistant
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```
2. In a separate terminal, run Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```
3. Open the Streamlit app in your browser and use the navigation menu.

## Folder Structure

- `app/`
  - `main.py` - FastAPI application entrypoint
  - `models/schemas.py` - Pydantic request and response models
  - `services/` - core AI and storage modules
    - `event_analyzer.py`
    - `topic_generator.py`
    - `fact_checker.py`
    - `history_manager.py`
    - `feedback_manager.py`
  - `storage/` - local JSON data files
- `tests/` - unit tests for modules and APIs
- `streamlit_app.py` - Streamlit frontend UI
- `requirements.txt` - Python dependencies

## API Endpoints

- `GET /` - health check
- `POST /analyze-event` - analyze event descriptions and extract themes
- `POST /generate-conversation` - generate conversation starters from themes
- `POST /fact-check` - verify topics using Wikipedia
- `GET /history` - fetch conversation history
- `POST /feedback` - submit feedback for a conversation

## Testing

Run tests with:

```bash
pytest
pytest -v
```

## Deployment

1. Activate the virtual environment
2. Run backend:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Run frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

FastAPI listens on `http://127.0.0.1:8000`, and Streamlit uses the API to load and save data.

## Demo

A quick demo flow is available in [demo/README.md](demo/README.md).

You can showcase the application by:
1. Running the app locally or using the deployed URL.
2. Entering an event name and description.
3. Clicking "Analyze Event" and then "Generate Conversation Starters".
4. Reviewing the generated themes, conversation starters, and fact checks.

## Future Scope

- Add authentication and user accounts
- Create a database-backed persistence layer
- Use larger transformer models for higher-quality text
- Improve UI with multi-step workflows
- Add more advanced fact-checking and citation support

## Conclusion

This project demonstrates a beginner-friendly AI web application with a modular architecture, integrating DistilBERT theme extraction, GPT-2 text generation, and Wikipedia fact verification. It helps users prepare more confident networking conversations, save results locally, and gather feedback for continuous improvement.
