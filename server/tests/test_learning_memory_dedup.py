import asyncio

from app.learning.memory_sink import LearningMemorySink
from app.learning.engine import LearningEngine
from app.memory.fake_gateway import FakeMemoryGateway


def test_duplicate_learning_is_not_persisted_twice():
    async def run():
        memory = FakeMemoryGateway()
        sink = LearningMemorySink(memory)
        engine = LearningEngine()

        first = engine.build_candidate(
            "Python uses indentation.",
            source="teacher",
            category="knowledge",
            confidence=0.95,
            should_remember=True,
        )

        second = engine.build_candidate(
            "  Python uses indentation.  ",
            source="teacher",
            category="knowledge",
            confidence=0.95,
            should_remember=True,
        )

        first_result = await sink.persist(first)
        second_result = await sink.persist(second)

        assert first_result.accepted is True
        assert second_result.accepted is False
        assert second_result.reason == "duplicate"
        assert len(memory.saved) == 1

    asyncio.run(run())
