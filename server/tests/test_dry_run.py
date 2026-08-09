from app.learning.dry_run import DryRunRunner
from app.learning.execution_boundary import ExecutionBoundary
from app.learning.execution_plan import ExecutionPlan


def plan():
    return ExecutionPlan(
        proposal_id="proposal-dry-1",
        target="local_ai",
        objective="Improve code retrieval",
        files=(
            "app/learning/code_intent.py",
            "app/learning/code_retriever.py",
        ),
        steps=("Prepare proposed change.",),
        validation_steps=("Run tests.",),
        metadata={
            "execution": "not_performed",
            "requires_authorization": True,
        },
    )


def test_dry_run_reports_blocked_execution():
    authorization = ExecutionBoundary().authorize(
        proposal_id="proposal-dry-1",
        review_status="pending",
        approved=False,
        validation_passed=True,
    )

    report = DryRunRunner().preview(plan(), authorization)

    assert report.execution_allowed is False
    assert report.execution_reason == "human_approval_required"
    assert report.files == (
        "app/learning/code_intent.py",
        "app/learning/code_retriever.py",
    )


def test_dry_run_reports_authorized_execution_without_executing():
    authorization = ExecutionBoundary().authorize(
        proposal_id="proposal-dry-1",
        review_status="approved",
        approved=True,
        validation_passed=True,
        approved_proposal_id="proposal-dry-1",
    )

    report = DryRunRunner().preview(plan(), authorization)

    assert report.execution_allowed is True
    assert report.execution_reason == "execution_authorized"
    assert report.objective == "Improve code retrieval"
    assert report.files


def test_dry_run_is_only_a_report():
    report = DryRunRunner().preview(
        plan(),
        ExecutionBoundary().authorize(
            proposal_id="proposal-dry-1",
            review_status="pending",
            approved=False,
            validation_passed=False,
        ),
    )

    assert report.execution_allowed is False
    assert report.execution_reason == "human_approval_required"
