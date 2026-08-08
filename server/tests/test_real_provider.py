import asyncio

import httpx
import pytest

from app.providers.real_provider import RealAIProvider


def test_real_provider_requires_api_key(monkeypatch):
    monkeypatch.delenv("AI_API_KEY", raising=False)
    monkeypatch.setenv("AI_API_ENDPOINT", "https://example.com/ai")

    provider = RealAIProvider()

    with pytest.raises(RuntimeError, match="AI_API_KEY is not configured"):
        asyncio.run(provider.generate("HELLO"))


def test_real_provider_requires_endpoint(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    monkeypatch.delenv("AI_API_ENDPOINT", raising=False)

    provider = RealAIProvider()

    with pytest.raises(RuntimeError, match="AI_API_ENDPOINT is not configured"):
        asyncio.run(provider.generate("HELLO"))


def test_real_provider_parses_reply(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    monkeypatch.setenv("AI_API_ENDPOINT", "https://teacher.test/ai")

    class MockClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, endpoint, json, headers):
            assert endpoint == "https://teacher.test/ai"
            assert json["message"] == "HELLO TEACHER"
            assert headers["Authorization"] == "Bearer test-key"

            request = httpx.Request(
                "POST",
                endpoint,
                headers=headers,
            )

            return httpx.Response(
                200,
                json={"reply": "Hello from Teacher AI"},
                request=request,
            )

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda timeout: MockClient(),
    )

    provider = RealAIProvider()

    reply = asyncio.run(
        provider.generate(
            "HELLO TEACHER",
            conversation_id="test-conversation",
        )
    )

    assert reply == "Hello from Teacher AI"
