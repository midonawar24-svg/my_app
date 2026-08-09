from dataclasses import dataclass

from typing import Any


@dataclass(frozen=True)
class EvolutionReport:
    learning_accepted: bool
    proposal_id: str | None
    evaluation_accepted: bool | None
    review_status: str | None
    execution_allowed: bool | None
    dry_run_available: bool
    dry_run_files: tuple[str, ...]
    execution_reason: str | None


class EvolutionReportBuilder:
    """
    Builds a read-only summary of the learning/evolution lifecycle.

    It does not execute, modify, or approve anything.
    """

    def build(self, result: Any) -> EvolutionReport:
        learning_accepted = bool(
            getattr(result.learning, "accepted", False)
        )

        proposal_id = None
        evaluation_accepted = None

        if result.evolution is not None:
            proposal_id = result.evolution.proposal.proposal_id
            evaluation_accepted = result.evolution.evaluation.accepted

        review_status = None
        if result.review is not None:
            review_status = result.review.status

        execution_allowed = None
        execution_reason = None

        if result.execution is not None:
            execution_allowed = result.execution.allowed
            execution_reason = result.execution.reason

        dry_run_files: tuple[str, ...] = ()

        if result.dry_run is not None:
            dry_run_files = result.dry_run.files

        return EvolutionReport(
            learning_accepted=learning_accepted,
            proposal_id=proposal_id,
            evaluation_accepted=evaluation_accepted,
            review_status=review_status,
            execution_allowed=execution_allowed,
            dry_run_available=result.dry_run is not None,
            dry_run_files=dry_run_files,
            execution_reason=execution_reason,
        )
