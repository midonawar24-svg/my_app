from app.learning.evolution_models import (
    EvolutionEvaluation,
    EvolutionProposal,
)


class EvolutionEngine:
    """
    Evaluates proposed improvements before they can enter
    the evolution/memory pipeline.

    It does not modify production code by itself.
    """

    def evaluate(
        self,
        proposal: EvolutionProposal,
    ) -> EvolutionEvaluation:
        if not proposal.proposal_id.strip():
            return EvolutionEvaluation(
                proposal_id="",
                accepted=False,
                score=0.0,
                reason="missing_proposal_id",
            )

        if not proposal.title.strip():
            return EvolutionEvaluation(
                proposal_id=proposal.proposal_id,
                accepted=False,
                score=0.0,
                reason="missing_title",
            )

        if not 0.0 <= proposal.expected_gain <= 1.0:
            return EvolutionEvaluation(
                proposal_id=proposal.proposal_id,
                accepted=False,
                score=0.0,
                reason="invalid_expected_gain",
            )

        if not 0.0 <= proposal.confidence <= 1.0:
            return EvolutionEvaluation(
                proposal_id=proposal.proposal_id,
                accepted=False,
                score=0.0,
                reason="invalid_confidence",
            )

        if not 0.0 <= proposal.risk <= 1.0:
            return EvolutionEvaluation(
                proposal_id=proposal.proposal_id,
                accepted=False,
                score=0.0,
                reason="invalid_risk",
            )

        score = (
            proposal.expected_gain * 0.50
            + proposal.confidence * 0.35
            + (1.0 - proposal.risk) * 0.15
        )

        accepted = score >= 0.70

        return EvolutionEvaluation(
            proposal_id=proposal.proposal_id,
            accepted=accepted,
            score=score,
            reason="accepted" if accepted else "score_too_low",
            evidence=list(proposal.evidence),
            metadata={
                "category": proposal.category,
                "target": proposal.target,
            },
        )
