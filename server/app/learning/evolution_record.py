from typing import Any

from app.learning.evolution_models import (
    EvolutionEvaluation,
    EvolutionProposal,
)
from app.learning.evolution_store import EvolutionStore
from app.learning.validation_gate import ValidationReport


class EvolutionRecordService:
    """
    Combines model evaluation and validation evidence into the
    persistent evolution history.

    It records evidence only. It does not modify production code.
    """

    def __init__(self, store: EvolutionStore):
        self.store = store

    def record(
        self,
        proposal: EvolutionProposal,
        evaluation: EvolutionEvaluation,
        validation: ValidationReport,
    ) -> None:
        metadata: dict[str, Any] = dict(evaluation.metadata)

        metadata["validation"] = {
            "passed": validation.passed,
            "score": validation.score,
            "checks": list(validation.checks),
            "failures": list(validation.failures),
            "metadata": dict(validation.metadata),
        }

        enriched_evaluation = EvolutionEvaluation(
            proposal_id=evaluation.proposal_id,
            accepted=evaluation.accepted and validation.passed,
            score=evaluation.score,
            reason=(
                "accepted_and_validated"
                if evaluation.accepted and validation.passed
                else "validation_failed"
                if evaluation.accepted
                else evaluation.reason
            ),
            evidence=[
                *evaluation.evidence,
                *validation.checks,
            ],
            metadata=metadata,
        )

        self.store.record(proposal, enriched_evaluation)
