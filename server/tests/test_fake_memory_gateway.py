import asyncio

from app.memory.fake_gateway import FakeMemoryGateway


def test_fake_memory_gateway_saves_memory():
    async def run():
        gateway = FakeMemoryGateway()

        result = await gateway.remember(
            content="A validated fact.",
            conversation_id="memory-test",
            memory_type="knowledge",
            metadata={"source": "teacher"},
        )

        assert result.accepted is True
        assert result.memory_id == "memory-1"
        assert gateway.saved[0]["content"] == "A validated fact."
        assert gateway.saved[0]["memory_type"] == "knowledge"
        assert gateway.saved[0]["metadata"]["source"] == "teacher"

    asyncio.run(run())
