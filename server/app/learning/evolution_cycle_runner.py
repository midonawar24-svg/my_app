from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from app.events.bus import EvolutionEventBus
from app.events.models import EvolutionEvent
from app.learning.evolution_models import EvolutionCycle
from app.learning.evolution_store import EvolutionStore


@dataclass(frozen=True)
class EvolutionRunResult:
    cycle_id: str
    target: str
    started_at: str
    finished_at: str | None = None
    result: str = "started"
    metadata: dict[str, Any] = field(default_factory=dict)


class EvolutionCycleRunner:
    """
    Starts an evolution cycle through an injected orchestrator.

    This layer does not modify or execute project code itself.
    """

    def __init__(self, orchestrator=None, *, store=None, event_bus=None):
        self.orchestrator = orchestrator
        self.store = store
        self.event_bus = event_bus

    def run(
        self,
        *,
        target: str = "local_ai",
        context: dict[str, Any] | None = None,
    ):
        cycle_id = (
            f"run-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        )
        started_at = datetime.now(timezone.utc).isoformat()

        if self.orchestrator is None:
            return EvolutionRunResult(
                cycle_id=cycle_id,
                target=target,
                started_at=started_at,
                result="started",
                metadata={
                    "context": dict(context or {}),
                    "execution": "not_started",
                    "orchestrator": "not_configured",
                },
            )

        async def execute():
            try:
                evolution = await self.orchestrator.process_with_advisor(
                    target=target,
                    context=dict(context or {}),
                )

                finished_at = datetime.now(timezone.utc).isoformat()

                metadata = {
                    "proposal_id": evolution.proposal.proposal_id,
                    "accepted": evolution.evaluation.accepted,
                    "score": evolution.evaluation.score,
                    "execution": "not_started",
                }

                if self.store is not None:
                    self.store.record_cycle(
                        EvolutionCycle(
                            cycle_id=cycle_id,
                            target=target,
                            started_at=started_at,
                            finished_at=finished_at,
                            duration_seconds=None,
                            result="completed",
                            metadata=metadata,
                        )
                    )

                if self.event_bus is not None:
                    self.event_bus.publish(
                        EvolutionEvent(
                            event_id=f"{cycle_id}:completed",
                            event_type="evolution.cycle_completed",
                            source="evolution_cycle_runner",
                            payload={
                                "cycle_id": cycle_id,
                                "target": target,
                                **metadata,
                            },
                        )
                    )

                return EvolutionRunResult(
                    cycle_id=cycle_id,
                    target=target,
                    started_at=started_at,
                    finished_at=finished_at,
                    result="completed",
                    metadata=metadata,
                )

            except Exception as exc:
                finished_at = datetime.now(timezone.utc).isoformat()

                metadata = {
                    "execution": "not_started",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }

                if self.store is not None:
                    self.store.record_cycle(
                        EvolutionCycle(
                            cycle_id=cycle_id,
                            target=target,
                            started_at=started_at,
                            finished_at=finished_at,
                            duration_seconds=None,
                            result="error",
                            metadata=metadata,
                        )
                    )

                if self.event_bus is not None:
                    self.event_bus.publish(
                        EvolutionEvent(
                            event_id=f"{cycle_id}:failed",
                            event_type="evolution.cycle_failed",
                            source="evolution_cycle_runner",
                            payload={
                                "cycle_id": cycle_id,
                                "target": target,
                                **metadata,
                            },
                        )
                    )

                raise

        return execute()
