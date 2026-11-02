"""Smoke tests for the FastAPI application."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "FinAgent API is running",
    }


def test_run_agent_requires_goal_and_start_url():
    response = client.post("/run-agent", json={})

    assert response.status_code == 422