from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionAuthorization:
    allowed: bool
    reason: str


class ExecutionBoundary:
    """
    Final authorization boundary before any evolution execution.

    This class does not execute or modify project code.
    It only decides whether execution is authorized.
    """

    def authorize(
        self,
        *,
        proposal_id: str,
        review_status: str,
        approved: bool,
        validation_passed: bool,
        approved_proposal_id: str | None = None,
    ) -> ExecutionAuthorization:

        if not proposal_id.strip():
            return ExecutionAuthorization(
                allowed=False,
                reason="missing_proposal_id",
            )

        if review_status != "approved" or not approved:
            return ExecutionAuthorization(
                allowed=False,
                reason="human_approval_required",
            )

        if not validation_passed:
            return ExecutionAuthorization(
                allowed=False,
                reason="validation_required",
            )

        if approved_proposal_id != proposal_id:
            return ExecutionAuthorization(
                allowed=False,
                reason="proposal_approval_mismatch",
            )

        return ExecutionAuthorization(
            allowed=True,
            reason="execution_authorized",
        )
