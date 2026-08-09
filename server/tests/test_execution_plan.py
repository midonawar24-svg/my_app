import pytest

from app.learning.execution_plan import ExecutionPlanBuilder


def test_execution_plan_builds_reviewable_plan():
    builder = ExecutionPlanBuilder()

    plan = builder.build(
        proposal_id="proposal-1",
        target="local_ai",
        objective="Improve code retrieval",
        files=(
            "app/learning/code_intent.py",
            "app/learning/code_retriever.py",
        ),
    )

    assert plan.proposal_id == "proposal-1"
    assert plan.target == "local_ai"
    assert plan.objective == "Improve code retrieval"

    assert plan.files == (
        "app/learning/code_intent.py",
        "app/learning/code_retriever.py",
    )

    assert plan.steps
    assert plan.validation_steps

    assert plan.metadata["execution"] == "not_performed"
    assert plan.metadata["requires_authorization"] is True


def test_execution_plan_rejects_missing_proposal():
    builder = ExecutionPlanBuilder()

    with pytest.raises(ValueError, match="proposal_id"):
        builder.build(
            proposal_id="",
            target="local_ai",
            objective="Improve retrieval",
        )


def test_execution_plan_rejects_missing_target():
    builder = ExecutionPlanBuilder()

    with pytest.raises(ValueError, match="target"):
        builder.build(
            proposal_id="proposal-2",
            target="",
            objective="Improve retrieval",
        )


def test_execution_plan_rejects_missing_objective():
    builder = ExecutionPlanBuilder()

    with pytest.raises(ValueError, match="objective"):
        builder.build(
            proposal_id="proposal-3",
            target="local_ai",
            objective="",
        )
