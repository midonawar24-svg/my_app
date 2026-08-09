import asyncio

from app.learning.memory_sink import LearningMemorySink
from app.learning.pipeline import LearningPipeline
from app.memory.fake_gateway import FakeMemoryGateway


class FakeTeacherGateway:
    async def ask(
        self,
        message,
        conversation_id=None,
        context=None,
    ):
        return "Learned behavior"


def test_learning_provenance_reaches_memory():
    async def run():
        memory = FakeMemoryGateway()
        pipeline = LearningPipeline(
            FakeTeacherGateway(),
            LearningMemorySink(memory),
        )

        result = await pipeline.learn(
            "Teach me a behavior",
            conversation_id="provenance-test",
            source="teacher",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
        )

        assert result.accepted is True
        assert len(memory.saved) == 1

        saved = memory.saved[0]
        metadata = saved["metadata"]

        assert metadata["learning_source"] == "teacher"
        assert metadata["learning_category"] == "knowledge"
        assert metadata["normalized"] is True

    asyncio.run(run())
