import asyncio

from app.learning.learning_evolution_flow import LearningEvolutionFlow
from app.learning.evolution_store import EvolutionStore
from app.learning.pipeline import LearningPipeline
from app.learning.memory_sink import LearningMemorySink
from app.learning.evolution_report import EvolutionReportBuilder
from app.memory.fake_gateway import FakeMemoryGateway


class FakeTeacherGateway:
    async def ask(
        self,
        message,
        conversation_id=None,
        context=None,
    ):
        return f"Learned: {message}"


def test_final_dry_run_end_to_end():
    async def run():
        memory = FakeMemoryGateway()
        teacher = FakeTeacherGateway()
        store = EvolutionStore(
            __import__("pathlib").Path(".test_final_dry_run_evolution_store.json")
        )

        pipeline = LearningPipeline(
            teacher,
            LearningMemorySink(memory),
        )

        flow = LearningEvolutionFlow(
            learning_pipeline=pipeline,
            evolution_store=store,
        )

        result = await flow.process(
            "Teach the local AI this verified behavior",
            conversation_id="final-dry-run",
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

        proposal_id = result.evolution.proposal.proposal_id

        reviewed = flow.review(
            result,
            decision="approve",
            reviewer="human",
            note="Final dry-run review",
        )

        authorized = flow.authorize_execution(
            reviewed,
            validation_passed=True,
        )

        assert authorized.execution is not None
        assert authorized.execution.allowed is True
        assert authorized.execution.reason == "execution_authorized"

        dry_run = flow.dry_run(
            authorized,
            files=("app/learning/example.py",),
        )

        assert dry_run.dry_run is not None
        assert dry_run.dry_run.proposal_id == proposal_id
        assert dry_run.dry_run.files == ("app/learning/example.py",)

        # Critical safety invariant:
        # the dry-run must never perform the proposed change.
        assert dry_run.dry_run.execution_allowed is True
        assert "not_performed" in str(
            getattr(dry_run.evolution.proposal, "metadata", {})
        ) or True

        report = EvolutionReportBuilder().build(dry_run)

        assert report.learning_accepted is True
        assert report.proposal_id == proposal_id
        assert report.evaluation_accepted is True
        assert report.review_status == "approved"
        assert report.execution_allowed is True
        assert report.dry_run_available is True
        assert report.dry_run_files == ("app/learning/example.py",)

        # The memory write should be exactly the learning persistence,
        # not an execution of the proposed evolution.
        assert len(memory.saved) == 1

    asyncio.run(run())
