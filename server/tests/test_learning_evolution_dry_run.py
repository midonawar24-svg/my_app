from app.learning.dry_run import DryRunRunner
from app.learning.evolution_models import EvolutionEvaluation, EvolutionProposal
from app.learning.execution_boundary import ExecutionAuthorization
from app.learning.execution_plan import ExecutionPlanBuilder


def test_dry_run_preview_is_read_only():
    proposal = EvolutionProposal(
        proposal_id="proposal-dry-1",
        title="Improve local AI",
        description="Improve retrieval behavior",
        category="learning",
        target="local_ai",
        expected_gain=0.9,
        confidence=0.95,
        risk=0.1,
        evidence=["test:evidence"],
    )

    evaluation = EvolutionEvaluation(
        proposal_id=proposal.proposal_id,
        accepted=True,
        score=0.92,
        reason="accepted",
    )

    plan = ExecutionPlanBuilder().build_from_proposal(
        proposal,
        files=("app/learning/code_intent.py",),
    )

    authorization = ExecutionAuthorization(
        allowed=False,
        reason="human_approval_required",
    )

    report = DryRunRunner().preview(plan, authorization)

    assert report.proposal_id == proposal.proposal_id
    assert report.target == proposal.target
    assert report.objective == proposal.description
    assert report.files == ("app/learning/code_intent.py",)
    assert report.execution_allowed is False
    assert report.execution_reason == "human_approval_required"
    assert "not_performed" not in report.execution_reason


def test_dry_run_can_show_authorized_state_without_executing():
    proposal = EvolutionProposal(
        proposal_id="proposal-dry-2",
        title="Improve retrieval",
        description="Improve code retrieval",
        category="learning",
        target="local_ai",
        expected_gain=0.8,
        confidence=0.9,
        risk=0.1,
    )

    plan = ExecutionPlanBuilder().build_from_proposal(
        proposal,
        files=("app/learning/code_intent.py",),
    )

    authorization = ExecutionAuthorization(
        allowed=True,
        reason="execution_authorized",
    )

    report = DryRunRunner().preview(plan, authorization)

    assert report.proposal_id == "proposal-dry-2"
    assert report.execution_allowed is True
    assert report.execution_reason == "execution_authorized"
    assert report.files == ("app/learning/code_intent.py",)
