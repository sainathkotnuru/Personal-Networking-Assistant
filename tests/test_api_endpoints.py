from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_event_endpoint():
    response = client.post(
        "/analyze-event",
        json={"event_name": "Team Meetup", "description": "A workshop for product managers and designers."},
    )
    assert response.status_code == 200
    assert "themes" in response.json()


def test_fact_check_endpoint():
    response = client.post("/fact-check", json={"topic": "Artificial Intelligence"})
    assert response.status_code == 200
    assert "topic" in response.json()
