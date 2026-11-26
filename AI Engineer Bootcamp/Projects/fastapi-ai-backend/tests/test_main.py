from fastapi.testclient import TestClient

from app.main import app
from app.services import ollama_service


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the AI Backend",
        "status": "running"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_chat(monkeypatch):
    # Replace the real Ollama call with a mock response
    def mock_generate(prompt):
        return "RAG stands for Retrieval-Augmented Generation."

    monkeypatch.setattr(
        ollama_service,
        "generate_response",
        mock_generate
    )

    response = client.post(
        "/chat",
        json={"prompt": "Explain RAG"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "prompt": "Explain RAG",
        "response": "RAG stands for Retrieval-Augmented Generation."
    }


def test_chat_empty_prompt():
    response = client.post(
        "/chat",
        json={"prompt": ""}
    )

    assert response.status_code == 422