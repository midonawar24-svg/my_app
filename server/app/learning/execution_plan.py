from dataclasses import dataclass, field

from app.learning.evolution_models import EvolutionProposal


@dataclass(frozen=True)
class ExecutionPlan:
    proposal_id: str
    target: str
    objective: str
    files: tuple[str, ...] = ()
    steps: tuple[str, ...] = ()
    validation_steps: tuple[str, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)


class ExecutionPlanBuilder:
    """
    Converts an approved evolution proposal into a reviewable plan.

    This class never edits or executes project code.
    """

    def build_from_proposal(
        self,
        proposal: EvolutionProposal,
        *,
        files: tuple[str, ...] = (),
    ) -> ExecutionPlan:
        if not proposal.proposal_id.strip():
            raise ValueError("proposal_id cannot be empty")

        if not proposal.target.strip():
            raise ValueError("target cannot be empty")

        if not proposal.description.strip():
            raise ValueError("objective cannot be empty")

        return self.build(
            proposal_id=proposal.proposal_id,
            target=proposal.target,
            objective=proposal.description,
            files=files,
        )

    def build(
        self,
        *,
        proposal_id: str,
        target: str,
        objective: str,
        files: tuple[str, ...] = (),
    ) -> ExecutionPlan:
        if not proposal_id.strip():
            raise ValueError("proposal_id cannot be empty")

        if not target.strip():
            raise ValueError("target cannot be empty")

        if not objective.strip():
            raise ValueError("objective cannot be empty")

        return ExecutionPlan(
            proposal_id=proposal_id,
            target=target,
            objective=objective.strip(),
            files=tuple(files),
            steps=(
                "Inspect the selected files.",
                "Prepare a minimal proposed change.",
                "Keep the original implementation unchanged.",
            ),
            validation_steps=(
                "Run syntax validation.",
                "Run relevant automated tests.",
                "Reject the plan if validation fails.",
            ),
            metadata={
                "execution": "not_performed",
                "requires_authorization": True,
            },
        )
