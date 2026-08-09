from dataclasses import dataclass, field
from typing import Any

from app.learning.evolution_models import EvolutionProposal


@dataclass(frozen=True)
class ChangePlan:
    proposal_id: str
    target: str
    objective: str
    steps: list[str] = field(default_factory=list)
    validation_steps: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ProposalRunner:
    """
    Converts an evolution proposal into a safe, testable change plan.

    This class does not edit source files and does not execute arbitrary
    model-generated code.
    """

    def build_plan(
        self,
        proposal: EvolutionProposal,
    ) -> ChangePlan:
        if not proposal.proposal_id.strip():
            raise ValueError("Proposal ID cannot be empty")

        if not proposal.target.strip():
            raise ValueError("Proposal target cannot be empty")

        if not proposal.description.strip():
            raise ValueError("Proposal description cannot be empty")

        steps = [
            "Inspect the current implementation.",
            "Identify the smallest safe change.",
            "Prepare the proposed patch separately.",
            "Run syntax and static validation.",
            "Run the relevant automated tests.",
            "Compare the result against the current implementation.",
        ]

        validation_steps = [
            "python -m compileall app",
            "Run project tests if available.",
            "Reject the proposal if validation fails.",
            "Keep the original implementation unchanged until approval.",
        ]

        return ChangePlan(
            proposal_id=proposal.proposal_id,
            target=proposal.target,
            objective=proposal.description.strip(),
            steps=steps,
            validation_steps=validation_steps,
            metadata={
                "category": proposal.category,
                "expected_gain": proposal.expected_gain,
                "confidence": proposal.confidence,
                "risk": proposal.risk,
            },
        )
