import asyncio

from app.events.bus import EvolutionEventBus
from app.learning.evolution_cycle_runner import EvolutionCycleRunner
from app.learning.evolution_store import EvolutionStore


class FinalStubOrchestrator:
    def __init__(self):
        self.calls = []

    async def process_with_advisor(self, *, target, context):
        self.calls.append({
            "target": target,
            "context": context,
        })

        return type(
            "Evolution",
            (),
            {
                "proposal": type(
                    "Proposal",
                    (),
                    {"proposal_id": "proposal-9-6"},
                )(),
                "evaluation": type(
                    "Evaluation",
                    (),
                    {
                        "accepted": True,
                        "score": 0.96,
                    },
                )(),
            },
        )()


def test_final_cycle_runner_e2e(tmp_path):
    async def run():
        store = EvolutionStore(tmp_path / "evolution.json")
        bus = EvolutionEventBus()
        events = []

        bus.subscribe(
            "evolution.cycle_completed",
            lambda event: events.append(event),
        )

        orchestrator = FinalStubOrchestrator()

        runner = EvolutionCycleRunner(
            orchestrator,
            store=store,
            event_bus=bus,
        )

        result = await runner.run(
            target="local_ai",
            context={
                "domain_count": 16,
                "stage": 9,
            },
        )

        assert result.cycle_id.startswith("run-")
        assert result.target == "local_ai"
        assert result.result == "completed"
        assert result.started_at
        assert result.finished_at is not None

        assert result.metadata["proposal_id"] == "proposal-9-6"
        assert result.metadata["accepted"] is True
        assert result.metadata["score"] == 0.96
        assert result.metadata["execution"] == "not_started"

        assert len(orchestrator.calls) == 1
        assert orchestrator.calls[0]["target"] == "local_ai"
        assert orchestrator.calls[0]["context"]["stage"] == 9

        history = store.history()
        cycles = [
            record["cycle"]
            for record in history
            if "cycle" in record
        ]

        assert len(cycles) == 1

        cycle = cycles[0]
        assert cycle["cycle_id"] == result.cycle_id
        assert cycle["target"] == "local_ai"
        assert cycle["result"] == "completed"
        assert cycle["metadata"]["proposal_id"] == "proposal-9-6"
        assert cycle["metadata"]["accepted"] is True
        assert cycle["metadata"]["score"] == 0.96
        assert cycle["metadata"]["execution"] == "not_started"

        assert len(events) == 1

        event = events[0]
        assert event.event_type == "evolution.cycle_completed"
        assert event.source == "evolution_cycle_runner"
        assert event.payload["cycle_id"] == result.cycle_id
        assert event.payload["proposal_id"] == "proposal-9-6"
        assert event.payload["accepted"] is True
        assert event.payload["score"] == 0.96
        assert event.payload["execution"] == "not_started"

    asyncio.run(run())
