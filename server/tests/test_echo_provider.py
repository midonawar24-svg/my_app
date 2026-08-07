import asyncio
from app.providers.echo_provider import EchoProvider

def test_echo_provider_returns_echo():
    async def run():
        provider = EchoProvider()
        reply = await provider.generate("مرحبا", conversation_id="test-123")
        assert reply == "Echo: مرحبا"
        reply2 = await provider.generate("hi", context={"user": "test"})
        assert reply2 == "Echo: hi"
    asyncio.run(run())
