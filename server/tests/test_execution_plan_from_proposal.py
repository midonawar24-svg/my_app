from app.learning.evolution_models import EvolutionProposal
from app.learning.execution_plan import ExecutionPlanBuilder


def test_execution_plan_preserves_proposal_data():
    proposal = EvolutionProposal(
        proposal_id="proposal-42",
        title="Improve retrieval",
        description="Improve Arabic and English code retrieval",
        category="code_retrieval",
        target="local_ai",
        expected_gain=0.9,
        confidence=0.95,
        risk=0.1,
    )

    plan = ExecutionPlanBuilder().build_from_proposal(
        proposal,
        files=(
            "app/learning/code_intent.py",
            "app/learning/code_retriever.py",
        ),
    )

    assert plan.proposal_id == proposal.proposal_id
    assert plan.target == proposal.target
    assert plan.objective == proposal.description
    assert plan.files == (
        "app/learning/code_intent.py",
        "app/learning/code_retriever.py",
    )

    assert plan.metadata["execution"] == "not_performed"
    assert plan.metadata["requires_authorization"] is True
