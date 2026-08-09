from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReviewDecision:
    approved: bool
    status: str
    reason: str
    metadata: dict[str, Any]


class HumanReviewGate:
    """
    Explicit approval boundary for evolution changes.

    AI may prepare and validate a proposal.
    Only explicit approval can mark it approved.

    This component never edits files and never executes code.
    """

    def review(
        self,
        *,
        proposal_id: str,
        decision: str,
        reviewer: str = "human",
        note: str = "",
    ) -> ReviewDecision:

        proposal_id = proposal_id.strip()
        decision = decision.strip().lower()
        reviewer = reviewer.strip() or "human"

        if not proposal_id:
            return ReviewDecision(
                approved=False,
                status="rejected",
                reason="missing_proposal_id",
                metadata={},
            )

        if decision == "approve":
            return ReviewDecision(
                approved=True,
                status="approved",
                reason="explicit_human_approval",
                metadata={
                    "proposal_id": proposal_id,
                    "reviewer": reviewer,
                    "note": note,
                },
            )

        if decision == "reject":
            return ReviewDecision(
                approved=False,
                status="rejected",
                reason="explicit_human_rejection",
                metadata={
                    "proposal_id": proposal_id,
                    "reviewer": reviewer,
                    "note": note,
                },
            )

        return ReviewDecision(
            approved=False,
            status="pending",
            reason="explicit_review_required",
            metadata={
                "proposal_id": proposal_id,
                "reviewer": reviewer,
                "note": note,
            },
        )
