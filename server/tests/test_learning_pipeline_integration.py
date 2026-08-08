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
        return f"Teacher learned: {message}"


def test_learning_pipeline_end_to_end():
    async def run():
        memory = FakeMemoryGateway()
        pipeline = LearningPipeline(
            FakeTeacherGateway(),
            LearningMemorySink(memory),
        )

        result = await pipeline.learn(
            "What is Python?",
            conversation_id="integration-test",
            source="teacher",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
            metadata={"test": True},
        )

        assert result.accepted is True
        assert result.memory_id == "memory-1"

        assert len(memory.saved) == 1

        saved = memory.saved[0]
        assert saved["content"] == "Teacher learned: What is Python?"
        assert saved["conversation_id"] == "integration-test"
        assert saved["memory_type"] == "knowledge"
        assert saved["metadata"]["source"] == "teacher"
        assert saved["metadata"]["confidence"] == 0.95
        assert saved["metadata"]["test"] is True

    asyncio.run(run())
