from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True
    assert data["service"] == "AI Core OS"


def test_versioned_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True


def test_chat():
    response = client.post(
        "/chat",
        json={
            "message": "مرحبا",
            "conversation_id": "test-123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reply"] == "Echo: مرحبا"
    assert data["conversation_id"] == "test-123"


def test_versioned_chat():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "hello",
            "conversationId": "test-456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reply"] == "Echo: hello"
    assert data["conversation_id"] == "test-456"
