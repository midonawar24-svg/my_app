import asyncio

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


def test_flow_execution_requires_review_and_validation():
    async def run():
        memory = FakeMemoryGateway()

        flow = LearningEvolutionFlow(
            LearningPipeline(
                FakeTeacherGateway(),
                LearningMemorySink(memory),
            )
        )

        result = await flow.process(
            "Learn a safe improvement",
            conversation_id="execution-integration",
            confidence=0.95,
            category="knowledge",
            should_remember=True,
            target="local_ai",
            expected_gain=0.90,
            risk=0.05,
        )

        assert result.evolution is not None

        pending = flow.review(
            result,
            decision="pending",
        )

        blocked = flow.authorize_execution(
            pending,
            validation_passed=True,
        )

        assert blocked.execution is not None
        assert blocked.execution.allowed is False
        assert blocked.execution.reason == "human_approval_required"

        approved = flow.review(
            result,
            decision="approve",
            reviewer="developer",
        )

        invalid = flow.authorize_execution(
            approved,
            validation_passed=False,
        )

        assert invalid.execution is not None
        assert invalid.execution.allowed is False
        assert invalid.execution.reason == "validation_required"

        authorized = flow.authorize_execution(
            approved,
            validation_passed=True,
        )

        assert authorized.execution is not None
        assert authorized.execution.allowed is True
        assert authorized.execution.reason == "execution_authorized"

    asyncio.run(run())
