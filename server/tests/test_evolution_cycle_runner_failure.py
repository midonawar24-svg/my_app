import asyncio

from app.events.bus import EvolutionEventBus
from app.learning.evolution_cycle_runner import EvolutionCycleRunner
from app.learning.evolution_store import EvolutionStore


class FailingOrchestrator:
    async def process_with_advisor(self, *, target, context):
        raise RuntimeError("advisor unavailable")


def test_runner_records_failure_and_publishes_event(tmp_path):
    async def run():
        store = EvolutionStore(tmp_path / "evolution.json")
        bus = EvolutionEventBus()
        received = []

        bus.subscribe(
            "evolution.cycle_failed",
            lambda event: received.append(event),
        )

        runner = EvolutionCycleRunner(
            FailingOrchestrator(),
            store=store,
            event_bus=bus,
        )

        try:
            await runner.run(
                target="local_ai",
                context={"domain_count": 16},
            )
        except RuntimeError as exc:
            assert str(exc) == "advisor unavailable"
        else:
            raise AssertionError("runner must propagate orchestrator failure")

        history = store.history()
        cycles = [
            record["cycle"]
            for record in history
            if "cycle" in record
        ]

        assert len(cycles) == 1
        assert cycles[0]["result"] == "error"
        assert cycles[0]["target"] == "local_ai"
        assert cycles[0]["metadata"]["execution"] == "not_started"
        assert cycles[0]["metadata"]["error_type"] == "RuntimeError"
        assert cycles[0]["metadata"]["error"] == "advisor unavailable"

        assert len(received) == 1
        event = received[0]

        assert event.event_type == "evolution.cycle_failed"
        assert event.source == "evolution_cycle_runner"
        assert event.payload["cycle_id"] == cycles[0]["cycle_id"]
        assert event.payload["target"] == "local_ai"
        assert event.payload["error_type"] == "RuntimeError"
        assert event.payload["execution"] == "not_started"

    asyncio.run(run())
