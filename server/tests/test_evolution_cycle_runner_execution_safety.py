import asyncio

from app.learning.evolution_cycle_runner import EvolutionCycleRunner


class ExecutionTrapOrchestrator:
    async def process_with_advisor(self, *, target, context):
        return type(
            "Evolution",
            (),
            {
                "proposal": type(
                    "Proposal",
                    (),
                    {"proposal_id": "proposal-safety-1"},
                )(),
                "evaluation": type(
                    "Evaluation",
                    (),
                    {
                        "accepted": True,
                        "score": 0.99,
                    },
                )(),
            },
        )()


def test_runner_never_starts_execution():
    async def run():
        runner = EvolutionCycleRunner(
            ExecutionTrapOrchestrator(),
        )

        result = await runner.run(
            target="local_ai",
            context={"safety": True},
        )

        assert result.result == "completed"
        assert result.metadata["execution"] == "not_started"

        assert "execute" not in result.metadata
        assert "execution_started" not in result.metadata
        assert "authorization" not in result.metadata

    asyncio.run(run())
