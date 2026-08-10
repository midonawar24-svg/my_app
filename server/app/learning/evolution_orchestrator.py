from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

from app.events.bus import EvolutionEventBus
from app.events.factory import EvolutionEventFactory
from app.learning.evolution_advisor import EvolutionAdvisor
from app.learning.evolution_bridge import EvolutionBridge
from app.learning.evolution_engine import EvolutionEngine
from app.learning.evolution_models import EvolutionCycle, EvolutionEvaluation, EvolutionProposal
from app.learning.evolution_store import EvolutionStore
from app.learning.evolution_memory import EvolutionMemory
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
        evolution_store: EvolutionStore | None = None,
        evolution_advisor: EvolutionAdvisor | None = None,
        ai_provider=None,
        event_bus: EvolutionEventBus | None = None,
    ):
        self.store = evolution_store or EvolutionStore(
            Path(".evolution_store.json")
        )
        self.memory = EvolutionMemory(self.store)

        self.bridge = evolution_bridge or EvolutionBridge(
            evolution_memory=self.memory,
        )

        if evolution_advisor is not None:
            self.advisor = evolution_advisor
        elif ai_provider is not None:
            self.advisor = EvolutionAdvisor(ai_provider)
        else:
            self.advisor = None

        self.engine = evolution_engine or EvolutionEngine()
        self.event_bus = event_bus or EvolutionEventBus()
        self.event_factory = EvolutionEventFactory()

    async def process_with_advisor(
        self,
        *,
        target: str = "local_ai",
        context: dict[str, Any] | None = None,
    ) -> EvolutionFlowResult:
        if self.advisor is None:
            raise RuntimeError(
                "Evolution advisor is not configured"
            )

        discovery_context = dict(context or {})

        proposal = await self.advisor.propose(
            target=target,
            context=discovery_context,
        )

        evaluation = self.engine.evaluate(proposal)

        self.store.record(
            proposal,
            evaluation,
        )

        return EvolutionFlowResult(
            candidate=LearningCandidate(
                content=proposal.description,
                conversation_id=None,
                source="evolution_advisor",
                confidence=proposal.confidence,
                category=proposal.category,
                should_remember=False,
                metadata={
                    "advisor": True,
                    "proposal_id": proposal.proposal_id,
                },
            ),
            proposal=proposal,
            evaluation=evaluation,
        )

    def process(
        self,
        candidate: LearningCandidate,
        *,
        target: str = "local_ai",
        expected_gain: float = 0.0,
        risk: float = 0.0,
    ) -> EvolutionFlowResult:
        cycle_id = f"cycle-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        started_at = datetime.now(timezone.utc).isoformat()
        started_clock = perf_counter()

        try:
            proposal = self.bridge.build_proposal(
                candidate,
                target=target,
                expected_gain=expected_gain,
                risk=risk,
            )

            fingerprint = proposal.metadata.get("fingerprint", "")

            if self.store.has_seen_evolution(fingerprint):
                evaluation = EvolutionEvaluation(
                    proposal_id=proposal.proposal_id,
                    accepted=False,
                    score=0.0,
                    reason="evolution_already_seen",
                    evidence=list(proposal.evidence),
                    metadata={
                        "category": proposal.category,
                        "target": proposal.target,
                        "fingerprint": fingerprint,
                        "skipped": True,
                    },
                )

                finished_at = datetime.now(timezone.utc).isoformat()

                self.store.record_cycle(
                    EvolutionCycle(
                        cycle_id=cycle_id,
                        target=target,
                        started_at=started_at,
                        finished_at=finished_at,
                        duration_seconds=perf_counter() - started_clock,
                        result="duplicate_skipped",
                        metadata={
                            "proposal_id": proposal.proposal_id,
                            "fingerprint": fingerprint,
                        },
                    )
                )

                self.event_bus.publish(
                    self.event_factory.duplicate_skipped(
                        event_id=f"{cycle_id}:duplicate",
                        proposal_id=proposal.proposal_id,
                        target=target,
                        fingerprint=fingerprint,
                        reason=evaluation.reason,
                    )
                )

                return EvolutionFlowResult(
                    candidate=candidate,
                    proposal=proposal,
                    evaluation=evaluation,
                )

            evaluation = self.engine.evaluate(proposal)

            self.store.record(
                proposal,
                evaluation,
            )

            finished_at = datetime.now(timezone.utc).isoformat()

            self.store.record_cycle(
                EvolutionCycle(
                    cycle_id=cycle_id,
                    target=target,
                    started_at=started_at,
                    finished_at=finished_at,
                    duration_seconds=perf_counter() - started_clock,
                    result="evaluated",
                    metadata={
                        "proposal_id": proposal.proposal_id,
                        "accepted": evaluation.accepted,
                        "score": evaluation.score,
                    },
                )
            )

            self.event_bus.publish(
                self.event_factory.evaluated(
                    event_id=f"{cycle_id}:evaluated",
                    proposal_id=proposal.proposal_id,
                    target=target,
                    accepted=evaluation.accepted,
                    score=evaluation.score,
                    reason=evaluation.reason,
                )
            )

            return EvolutionFlowResult(
                candidate=candidate,
                proposal=proposal,
                evaluation=evaluation,
            )

        except Exception as exc:
            finished_at = datetime.now(timezone.utc).isoformat()

            self.store.record_cycle(
                EvolutionCycle(
                    cycle_id=cycle_id,
                    target=target,
                    started_at=started_at,
                    finished_at=finished_at,
                    duration_seconds=perf_counter() - started_clock,
                    result="error",
                    metadata={
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    },
                )
            )

            raise
