from app.learning.review_gate import HumanReviewGate


def test_review_pending():
    result = HumanReviewGate().review(
        proposal_id="proposal-1",
        decision="pending",
    )

    assert result.status == "pending"
    assert result.approved is False


def test_review_approve():
    result = HumanReviewGate().review(
        proposal_id="proposal-2",
        decision="approve",
        reviewer="developer",
        note="Looks safe",
    )

    assert result.status == "approved"
    assert result.approved is True
    assert result.reason == "explicit_human_approval"
    assert result.metadata["reviewer"] == "developer"
    assert result.metadata["note"] == "Looks safe"


def test_review_reject():
    result = HumanReviewGate().review(
        proposal_id="proposal-3",
        decision="reject",
        reviewer="developer",
    )

    assert result.status == "rejected"
    assert result.approved is False
    assert result.reason == "explicit_human_rejection"


def test_review_requires_proposal_id():
    result = HumanReviewGate().review(
        proposal_id="",
        decision="approve",
    )

    assert result.status == "rejected"
    assert result.approved is False
    assert result.reason == "missing_proposal_id"
