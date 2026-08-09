from app.learning.execution_boundary import ExecutionBoundary


def test_execution_requires_human_approval():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-1",
        review_status="pending",
        approved=False,
        validation_passed=True,
    )

    assert result.allowed is False
    assert result.reason == "human_approval_required"


def test_execution_requires_validation():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-2",
        review_status="approved",
        approved=True,
        validation_passed=False,
    )

    assert result.allowed is False
    assert result.reason == "validation_required"


def test_execution_requires_matching_approval():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-3",
        review_status="approved",
        approved=True,
        validation_passed=True,
        approved_proposal_id="different-proposal",
    )

    assert result.allowed is False
    assert result.reason == "proposal_approval_mismatch"


def test_execution_can_be_authorized():
    boundary = ExecutionBoundary()

    result = boundary.authorize(
        proposal_id="proposal-4",
        review_status="approved",
        approved=True,
        validation_passed=True,
        approved_proposal_id="proposal-4",
    )

    assert result.allowed is True
    assert result.reason == "execution_authorized"
