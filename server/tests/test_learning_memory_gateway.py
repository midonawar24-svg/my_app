import asyncio

from app.learning.memory_sink import LearningMemorySink
from app.learning.models import LearningCandidate
from app.memory.fake_gateway import FakeMemoryGateway


def test_learning_memory_sink_writes_to_memory_gateway():
    async def run():
        gateway = FakeMemoryGateway()
        sink = LearningMemorySink(gateway)

        candidate = LearningCandidate(
            content="A validated fact.",
            source="teacher",
            conversation_id="learning-test",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
            metadata={"source": "teacher"},
        )

        result = await sink.persist(candidate)

        assert result.accepted is True
        assert result.memory_id == "memory-1"
        assert len(gateway.saved) == 1
        assert gateway.saved[0]["content"] == "A validated fact."
        assert gateway.saved[0]["conversation_id"] == "learning-test"

    asyncio.run(run())
