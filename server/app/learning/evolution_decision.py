from dataclasses import dataclass
from typing import Any

from app.learning.evolution_models import EvolutionEvaluation


@dataclass(frozen=True)
class EvolutionDecision:
    status: str
    allowed: bool
    reason: str
    metadata: dict[str, Any]


class EvolutionDecisionLayer:
    """
    Final safety decision before any future human-approved change.

    This layer never edits files and never executes generated code.
    """

    def decide(
        self,
        *,
        learning_accepted: bool,
        evaluation: EvolutionEvaluation | None,
    ) -> EvolutionDecision:

        if not learning_accepted:
            return EvolutionDecision(
                status="not_eligible",
                allowed=False,
                reason="learning_not_accepted",
                metadata={},
            )

        if evaluation is None:
            return EvolutionDecision(
                status="rejected",
                allowed=False,
                reason="missing_evaluation",
                metadata={},
            )

        if not evaluation.accepted:
            return EvolutionDecision(
                status="rejected",
                allowed=False,
                reason=evaluation.reason,
                metadata={
                    "score": evaluation.score,
                    "proposal_id": evaluation.proposal_id,
                },
            )

        return EvolutionDecision(
            status="ready_for_review",
            allowed=True,
            reason="proposal_validated_for_review",
            metadata={
                "score": evaluation.score,
                "proposal_id": evaluation.proposal_id,
            },
        )
