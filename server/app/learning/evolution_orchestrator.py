from dataclasses import dataclass
from typing import Any

from app.learning.evolution_bridge import EvolutionBridge
from app.learning.evolution_engine import EvolutionEngine
from app.learning.evolution_models import EvolutionEvaluation, EvolutionProposal
from app.learning.models import LearningCandidate


@dataclass(frozen=True)
class EvolutionFlowResult:
    candidate: LearningCandidate
    proposal: EvolutionProposal
    evaluation: EvolutionEvaluation


class EvolutionOrchestrator:
    """
    Coordinates learning -> proposal -> evaluation.

    This layer does not edit or execute project code.
    """

    def __init__(
        self,
        evolution_bridge: EvolutionBridge | None = None,
        evolution_engine: EvolutionEngine | None = None,
    ):
        self.bridge = evolution_bridge or EvolutionBridge()
        self.engine = evolution_engine or EvolutionEngine()

    def process(
        self,
        candidate: LearningCandidate,
        *,
        target: str = "local_ai",
        expected_gain: float = 0.0,
        risk: float = 0.0,
    ) -> EvolutionFlowResult:
        proposal = self.bridge.build_proposal(
            candidate,
            target=target,
            expected_gain=expected_gain,
            risk=risk,
        )

        evaluation = self.engine.evaluate(proposal)

        return EvolutionFlowResult(
            candidate=candidate,
            proposal=proposal,
            evaluation=evaluation,
        )
