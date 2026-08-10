import asyncio

from app.learning.evolution_store import EvolutionStore

from app.learning.learning_evolution_flow import LearningEvolutionFlow
from app.learning.pipeline import LearningPipeline
from app.learning.memory_sink import LearningMemorySink
from app.memory.fake_gateway import FakeMemoryGateway


class FakeTeacherGateway:
    async def ask(
        self,
        message,
        conversation_id=None,
        context=None,
    ):
        return f"Learned: {message}"


def test_full_learning_evolution_review_flow(tmp_path):
    async def run():
        memory = FakeMemoryGateway()
        store = EvolutionStore(tmp_path / "evolution.json")

        pipeline = LearningPipeline(
            FakeTeacherGateway(),
            LearningMemorySink(memory),
        )

        flow = LearningEvolutionFlow(
            learning_pipeline=pipeline,
            evolution_store=store,
        )

        result = await flow.process(
            "Teach the system a safe improvement",
            conversation_id="review-flow-test",
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
        assert result.decision is not None
        assert result.decision.status == "ready_for_review"
        assert result.decision.allowed is True

        pending = flow.review(
            result,
            decision="pending",
        )

        assert pending.review is not None
        assert pending.review.status == "pending"
        assert pending.review.approved is False

        approved = flow.review(
            result,
            decision="approve",
            reviewer="developer",
            note="Approved after review",
        )

        assert approved.review is not None
        assert approved.review.status == "approved"
        assert approved.review.approved is True
        assert approved.review.metadata["proposal_id"] == (
            result.evolution.proposal.proposal_id
        )

        rejected = flow.review(
            result,
            decision="reject",
            reviewer="developer",
        )

        assert rejected.review is not None
        assert rejected.review.status == "rejected"
        assert rejected.review.approved is False

    asyncio.run(run())
