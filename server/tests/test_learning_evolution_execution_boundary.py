from app.learning.execution_boundary import ExecutionBoundary


def test_pending_review_blocks_execution():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-1",
        review_status="pending",
        approved=False,
        validation_passed=True,
        approved_proposal_id=None,
    )

    assert result.allowed is False
    assert result.reason == "human_approval_required"


def test_failed_validation_blocks_execution():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-2",
        review_status="approved",
        approved=True,
        validation_passed=False,
        approved_proposal_id="proposal-2",
    )

    assert result.allowed is False
    assert result.reason == "validation_required"


def test_matching_approval_and_validation_authorize_execution():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-3",
        review_status="approved",
        approved=True,
        validation_passed=True,
        approved_proposal_id="proposal-3",
    )

    assert result.allowed is True
    assert result.reason == "execution_authorized"
