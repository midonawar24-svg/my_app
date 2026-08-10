from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvolutionReport:
    learning_accepted: bool
    proposal_id: str | None
    evaluation_accepted: bool | None

    cycle_id: str | None
    cycle_duration_seconds: float | None
    cycle_result: str | None

    evolution_fingerprint: str | None
    is_duplicate: bool
    was_skipped: bool

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

        cycle_id = None
        cycle_duration_seconds = None
        cycle_result = None

        evolution_fingerprint = None
        is_duplicate = False
        was_skipped = False

        if result.evolution is not None:
            proposal = result.evolution.proposal
            evaluation = result.evolution.evaluation

            proposal_id = proposal.proposal_id
            evaluation_accepted = evaluation.accepted

            proposal_metadata = dict(
                getattr(proposal, "metadata", None) or {}
            )
            evaluation_metadata = dict(
                getattr(evaluation, "metadata", None) or {}
            )

            evaluation_reason = getattr(
                evaluation,
                "reason",
                None,
            )

            evolution_fingerprint = (
                proposal_metadata.get("fingerprint")
                or evaluation_metadata.get("fingerprint")
            )

            is_duplicate = (
                evaluation_reason == "evolution_already_seen"
                or bool(evaluation_metadata.get("skipped", False))
            )

            was_skipped = bool(
                evaluation_metadata.get("skipped", False)
            )

        cycle = getattr(result, "cycle", None)

        if cycle is not None:
            cycle_id = cycle.cycle_id
            cycle_duration_seconds = cycle.duration_seconds
            cycle_result = cycle.result

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
            cycle_id=cycle_id,
            cycle_duration_seconds=cycle_duration_seconds,
            cycle_result=cycle_result,
            evolution_fingerprint=evolution_fingerprint,
            is_duplicate=is_duplicate,
            was_skipped=was_skipped,
            review_status=review_status,
            execution_allowed=execution_allowed,
            dry_run_available=result.dry_run is not None,
            dry_run_files=dry_run_files,
            execution_reason=execution_reason,
        )
