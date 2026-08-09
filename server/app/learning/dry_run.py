from dataclasses import dataclass

from app.learning.execution_plan import ExecutionPlan
from app.learning.execution_boundary import ExecutionAuthorization


@dataclass(frozen=True)
class DryRunReport:
    proposal_id: str
    target: str
    objective: str
    files: tuple[str, ...]
    steps: tuple[str, ...]
    validation_steps: tuple[str, ...]
    execution_allowed: bool
    execution_reason: str


class DryRunRunner:
    """
    Produces a read-only execution preview.

    It never edits, writes, or executes project code.
    """

    def preview(
        self,
        plan: ExecutionPlan,
        authorization: ExecutionAuthorization,
    ) -> DryRunReport:
        return DryRunReport(
            proposal_id=plan.proposal_id,
            target=plan.target,
            objective=plan.objective,
            files=plan.files,
            steps=plan.steps,
            validation_steps=plan.validation_steps,
            execution_allowed=authorization.allowed,
            execution_reason=authorization.reason,
        )
