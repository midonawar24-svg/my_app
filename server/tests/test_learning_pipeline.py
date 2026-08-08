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
        return "Learned from teacher"


def test_learning_pipeline_persists_valid_candidate():
    async def run():
        memory = FakeMemoryGateway()
        sink = LearningMemorySink(memory)
        pipeline = LearningPipeline(FakeTeacherGateway(), sink)

        result = await pipeline.learn(
            "Teach me something",
            conversation_id="pipeline-test",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
        )

        assert result.accepted is True
        assert result.memory_id == "memory-1"
        assert len(memory.saved) == 1
        assert memory.saved[0]["content"] == "Learned from teacher"

    asyncio.run(run())
