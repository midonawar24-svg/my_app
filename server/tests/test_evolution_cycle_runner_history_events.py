import asyncio
from types import SimpleNamespace

from app.events.bus import EvolutionEventBus
from app.learning.evolution_cycle_runner import EvolutionCycleRunner
from app.learning.evolution_store import EvolutionStore


class StubOrchestrator:
    async def process_with_advisor(self, *, target, context):
        return SimpleNamespace(
            proposal=SimpleNamespace(
                proposal_id="proposal-9-3",
            ),
            evaluation=SimpleNamespace(
                accepted=True,
                score=0.93,
            ),
        )


def test_runner_records_cycle_and_publishes_event(tmp_path):
    async def run():
        store = EvolutionStore(tmp_path / "evolution.json")
        bus = EvolutionEventBus()
        received = []

        bus.subscribe(
            "evolution.cycle_completed",
            lambda event: received.append(event),
        )

        runner = EvolutionCycleRunner(
            StubOrchestrator(),
            store=store,
            event_bus=bus,
        )

        result = await runner.run(
            target="local_ai",
            context={"domain_count": 16},
        )

        assert result.result == "completed"
        assert result.finished_at is not None
        assert result.metadata["proposal_id"] == "proposal-9-3"
        assert result.metadata["accepted"] is True
        assert result.metadata["score"] == 0.93

        history = store.history()
        cycles = [
            record["cycle"]
            for record in history
            if "cycle" in record
        ]

        assert len(cycles) == 1
        assert cycles[0]["cycle_id"] == result.cycle_id
        assert cycles[0]["target"] == "local_ai"
        assert cycles[0]["result"] == "completed"

        assert len(received) == 1
        event = received[0]
        assert event.event_type == "evolution.cycle_completed"
        assert event.source == "evolution_cycle_runner"
        assert event.payload["cycle_id"] == result.cycle_id
        assert event.payload["proposal_id"] == "proposal-9-3"
        assert event.payload["accepted"] is True

    asyncio.run(run())
