import asyncio

import pytest

from app.services.ai_service import AIService


def test_echo_provider_from_environment(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "echo")

    service = AIService()

    assert service.provider_name == "echo"
    assert type(service.provider).__name__ == "EchoProvider"

    reply = asyncio.run(
        service.generate("HELLO", conversation_id="test-echo")
    )

    assert reply == "Echo: HELLO"


def test_fake_provider_from_environment(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")

    service = AIService()

    assert service.provider_name == "fake"
    assert type(service.provider).__name__ == "FakeProvider"

    reply = asyncio.run(
        service.generate("HELLO", conversation_id="test-fake")
    )

    assert reply == "Fake AI: استقبلت 'HELLO'"


def test_unknown_provider_fails(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "unknown-provider")

    with pytest.raises(ValueError, match="Unknown AI provider"):
        AIService()
