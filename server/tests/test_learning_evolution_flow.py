import asyncio
from app.learning.evolution_store import EvolutionStore

from app.learning.learning_evolution_flow import LearningEvolutionFlow
from app.learning.evolution_store import EvolutionStore
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


def test_learning_to_evolution_flow(tmp_path):
    async def run():
        memory = FakeMemoryGateway()

        pipeline = LearningPipeline(
            FakeTeacherGateway(),
            LearningMemorySink(memory),
        )

        store = EvolutionStore(
            tmp_path / "evolution.json"
        )

        flow = LearningEvolutionFlow(
            pipeline,
            evolution_orchestrator=None,
            evolution_store=store,
        )

        result = await flow.process(
            "Teach the local AI a successful pattern",
            conversation_id="flow-test",
            source="teacher",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
            target="local_ai",
            expected_gain=0.90,
            risk=0.05,
        )

        assert result.learning.accepted is True
        assert result.learning.candidate.content == (
            "Teacher learned: Teach the local AI a successful pattern"
        )

        assert result.evolution is not None
        assert result.evolution.evaluation.accepted is True

        assert len(memory.saved) == 1
        assert memory.saved[0]["content"] == (
            "Teacher learned: Teach the local AI a successful pattern"
        )

    asyncio.run(run())
