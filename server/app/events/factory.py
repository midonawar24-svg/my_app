from typing import Any

from app.events.models import EvolutionEvent


class EvolutionEventFactory:
    """
    Single construction boundary for evolution events.

    This class only creates immutable event objects.
    It does not publish, execute, or modify project code.
    """

    def evaluated(
        self,
        *,
        event_id: str,
        proposal_id: str,
        target: str,
        accepted: bool,
        score: float,
        reason: str,
    ) -> EvolutionEvent:
        return EvolutionEvent(
            event_id=event_id,
            event_type="evolution.evaluated",
            source="evolution_orchestrator",
            payload={
                "proposal_id": proposal_id,
                "target": target,
                "accepted": accepted,
                "score": score,
                "reason": reason,
            },
        )

    def duplicate_skipped(
        self,
        *,
        event_id: str,
        proposal_id: str,
        target: str,
        fingerprint: str,
        reason: str,
    ) -> EvolutionEvent:
        return EvolutionEvent(
            event_id=event_id,
            event_type="evolution.duplicate_skipped",
            source="evolution_orchestrator",
            payload={
                "proposal_id": proposal_id,
                "target": target,
                "fingerprint": fingerprint,
                "reason": reason,
            },
        )
