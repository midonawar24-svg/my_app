from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_echo_provider(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "echo")

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "HELLO API",
            "conversation_id": "test-api",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reply"] == "Echo: HELLO API"
    assert data["conversation_id"] == "test-api"


def test_chat_fake_provider(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "HELLO FAKE",
            "conversation_id": "test-fake",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reply"] == "Fake AI: استقبلت 'HELLO FAKE'"
    assert data["conversation_id"] == "test-fake"


def test_chat_rejects_empty_message():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422
