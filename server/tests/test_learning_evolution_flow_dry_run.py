import pytest

from app.learning.evolution_models import EvolutionProposal
from app.learning.learning_evolution_flow import LearningEvolutionFlow


def test_flow_dry_run_requires_execution_state():
    flow = LearningEvolutionFlow.__new__(LearningEvolutionFlow)

    result = type(
        "Result",
        (),
        {
            "learning": None,
            "evolution": None,
            "decision": None,
            "review": None,
            "execution": None,
        },
    )()

    preview = flow.dry_run(result)

    assert preview.dry_run is None


def test_flow_dry_run_builds_preview_after_authorization():
    flow = LearningEvolutionFlow.__new__(LearningEvolutionFlow)

    flow.execution_boundary = None

    proposal = EvolutionProposal(
        proposal_id="proposal-flow-dry-1",
        title="Improve retrieval",
        description="Improve Arabic and English retrieval",
        category="code_retrieval",
        target="local_ai",
        expected_gain=0.9,
        confidence=0.95,
        risk=0.1,
    )

    from app.learning.evolution_models import EvolutionEvaluation
    from app.learning.execution_boundary import ExecutionAuthorization

    evolution = type(
        "Evolution",
        (),
        {
            "proposal": proposal,
            "evaluation": EvolutionEvaluation(
                proposal_id=proposal.proposal_id,
                accepted=True,
                score=0.92,
                reason="accepted",
            ),
        },
    )()

    result = type(
        "Result",
        (),
        {
            "learning": None,
            "evolution": evolution,
            "decision": None,
            "review": None,
            "execution": ExecutionAuthorization(
                allowed=False,
                reason="human_approval_required",
            ),
        },
    )()

    preview = flow.dry_run(
        result,
        files=("app/learning/code_intent.py",),
    )

    assert preview.dry_run is not None
    assert preview.dry_run.proposal_id == proposal.proposal_id
    assert preview.dry_run.files == ("app/learning/code_intent.py",)
    assert preview.dry_run.execution_allowed is False
    assert preview.dry_run.execution_reason == "human_approval_required"
