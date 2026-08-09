from app.learning.evolution_decision import EvolutionDecisionLayer
from app.learning.evolution_models import EvolutionEvaluation


def test_not_eligible_when_learning_rejected():
    result = EvolutionDecisionLayer().decide(
        learning_accepted=False,
        evaluation=None,
    )

    assert result.status == "not_eligible"
    assert result.allowed is False
    assert result.reason == "learning_not_accepted"


def test_rejected_when_evaluation_fails():
    evaluation = EvolutionEvaluation(
        proposal_id="proposal-1",
        accepted=False,
        score=0.40,
        reason="score_too_low",
    )

    result = EvolutionDecisionLayer().decide(
        learning_accepted=True,
        evaluation=evaluation,
    )

    assert result.status == "rejected"
    assert result.allowed is False
    assert result.reason == "score_too_low"


def test_ready_for_review_when_evaluation_passes():
    evaluation = EvolutionEvaluation(
        proposal_id="proposal-2",
        accepted=True,
        score=0.92,
        reason="accepted",
    )

    result = EvolutionDecisionLayer().decide(
        learning_accepted=True,
        evaluation=evaluation,
    )

    assert result.status == "ready_for_review"
    assert result.allowed is True
    assert result.reason == "proposal_validated_for_review"
    assert result.metadata["proposal_id"] == "proposal-2"
    assert result.metadata["score"] == 0.92
