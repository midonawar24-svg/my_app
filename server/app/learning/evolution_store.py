import json
from pathlib import Path
from typing import Any

from app.learning.evolution_models import (
    EvolutionCycle,
    EvolutionEvaluation,
    EvolutionProposal,
)


class EvolutionStore:
    """
    Persistent append-only store for evolution proposals and evaluations.

    The store records history; it does not execute code changes.
    """

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text())
        except (OSError, json.JSONDecodeError):
            return []

        return data if isinstance(data, list) else []

    def _write(self, records: list[dict[str, Any]]) -> None:
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(records, ensure_ascii=False, indent=2)
        )
        temporary.replace(self.path)

    def record_cycle(self, cycle: EvolutionCycle) -> None:
        records = self._read()

        records.append(
            {
                "cycle": {
                    "cycle_id": cycle.cycle_id,
                    "target": cycle.target,
                    "started_at": cycle.started_at,
                    "finished_at": cycle.finished_at,
                    "duration_seconds": cycle.duration_seconds,
                    "result": cycle.result,
                    "metadata": dict(cycle.metadata),
                }
            }
        )

        self._write(records)

    def has_seen_evolution(self, fingerprint: str) -> bool:
        fingerprint = fingerprint.strip()

        if not fingerprint:
            return False

        for record in self._read():
            proposal = record.get("proposal", {})
            metadata = proposal.get("metadata", {})

            if metadata.get("fingerprint") == fingerprint:
                return True

        return False

    def record(
        self,
        proposal: EvolutionProposal,
        evaluation: EvolutionEvaluation,
    ) -> None:
        records = self._read()

        records.append(
            {
                "proposal": {
                    "proposal_id": proposal.proposal_id,
                    "title": proposal.title,
                    "description": proposal.description,
                    "category": proposal.category,
                    "target": proposal.target,
                    "expected_gain": proposal.expected_gain,
                    "confidence": proposal.confidence,
                    "risk": proposal.risk,
                    "evidence": list(proposal.evidence),
                    "metadata": dict(proposal.metadata),
                },
                "evaluation": {
                    "proposal_id": evaluation.proposal_id,
                    "accepted": evaluation.accepted,
                    "score": evaluation.score,
                    "reason": evaluation.reason,
                    "evidence": list(evaluation.evidence),
                    "metadata": dict(evaluation.metadata),
                },
            }
        )

        self._write(records)

    def history(self) -> list[dict[str, Any]]:
        return self._read()

    def best(self, limit: int = 10) -> list[dict[str, Any]]:
        records = self._read()

        records.sort(
            key=lambda item: float(
                item.get("evaluation", {}).get("score", 0.0)
            ),
            reverse=True,
        )

        return records[:max(0, limit)]
