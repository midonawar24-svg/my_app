import asyncio

from app.events.bus import EvolutionEventBus
from app.learning.evolution_store import EvolutionStore
from app.learning.learning_evolution_flow import LearningEvolutionFlow
from app.learning.memory_sink import LearningMemorySink
from app.learning.pipeline import LearningPipeline
from app.memory.fake_gateway import FakeMemoryGateway


class FakeTeacherGateway:
    async def ask(self, message, conversation_id=None, context=None):
        return f"Teacher learned: {message}"


def test_flow_injects_isolated_store_and_event_bus(tmp_path):
    async def run():
        memory = FakeMemoryGateway()

        pipeline = LearningPipeline(
            FakeTeacherGateway(),
            LearningMemorySink(memory),
        )

        store = EvolutionStore(tmp_path / "evolution.json")
        bus = EvolutionEventBus()
        received = []

        bus.subscribe(
            "evolution.evaluated",
            lambda event: received.append(event),
        )

        flow = LearningEvolutionFlow(
            learning_pipeline=pipeline,
            evolution_store=store,
            event_bus=bus,
        )

        result = await flow.process(
            "Teach the local AI an isolated dependency contract",
            conversation_id="dependency-test",
            source="teacher",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
            target="local_ai",
            expected_gain=0.90,
            risk=0.05,
        )

        assert result.learning.accepted is True
        assert result.evolution is not None
        assert result.evolution.evaluation.accepted is True

        history = store.history()

        assert any("proposal" in record for record in history)
        assert any("cycle" in record for record in history)

        assert len(received) == 1
        assert received[0].event_type == "evolution.evaluated"
        assert received[0].payload["proposal_id"] == (
            result.evolution.proposal.proposal_id
        )

        assert not (tmp_path / "evolution.json").exists() is False

    asyncio.run(run())
