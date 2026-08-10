import asyncio
from types import SimpleNamespace

from app.learning.evolution_cycle_runner import EvolutionCycleRunner


class StubOrchestrator:
    def __init__(self):
        self.calls = []

    async def process_with_advisor(self, *, target, context):
        self.calls.append({
            "target": target,
            "context": context,
        })

        return SimpleNamespace(
            proposal=SimpleNamespace(
                proposal_id="proposal-runner-1",
            ),
            evaluation=SimpleNamespace(
                accepted=True,
                score=0.95,
            ),
        )


def test_runner_wires_to_orchestrator():
    async def run():
        orchestrator = StubOrchestrator()
        runner = EvolutionCycleRunner(orchestrator)

        result = await runner.run(
            target="local_ai",
            context={"domain_count": 16},
        )

        assert result.cycle_id.startswith("run-")
        assert result.result == "completed"
        assert result.finished_at is not None
        assert result.metadata["proposal_id"] == "proposal-runner-1"
        assert result.metadata["accepted"] is True
        assert result.metadata["score"] == 0.95
        assert result.metadata["execution"] == "not_started"

        assert len(orchestrator.calls) == 1
        assert orchestrator.calls[0]["target"] == "local_ai"
        assert orchestrator.calls[0]["context"]["domain_count"] == 16

    asyncio.run(run())


def test_runner_does_not_execute_project_changes():
    async def run():
        orchestrator = StubOrchestrator()
        runner = EvolutionCycleRunner(orchestrator)

        result = await runner.run(
            target="local_ai",
            context={},
        )

        assert result.metadata["execution"] == "not_started"

    asyncio.run(run())
