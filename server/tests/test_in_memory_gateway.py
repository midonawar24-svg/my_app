import asyncio

from app.memory.in_memory_gateway import InMemoryMemoryGateway


def test_in_memory_gateway_saves_memory():
    async def run():
        gateway = InMemoryMemoryGateway()

        result = await gateway.remember(
            content="A validated fact.",
            conversation_id="memory-test",
            memory_type="knowledge",
            metadata={"source": "teacher"},
        )

        assert result.accepted is True
        assert result.memory_id == "memory-1"
        assert gateway.saved[0]["content"] == "A validated fact."
        assert gateway.saved[0]["metadata"]["source"] == "teacher"

    asyncio.run(run())
