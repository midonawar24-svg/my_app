from dataclasses import dataclass
from typing import Any

from app.learning.evolution_store import EvolutionStore


@dataclass(frozen=True)
class EvolutionMemorySummary:
    total: int
    accepted: int
    rejected: int
    best_score: float
    successful_patterns: list[str]
    failed_patterns: list[str]


class EvolutionMemory:
    """
    Read-only intelligence layer over EvolutionStore.

    It does not modify proposals, execute code, or change production files.
    """

    def __init__(self, store: EvolutionStore):
        self.store = store

    def history(self) -> list[dict[str, Any]]:
        return self.store.history()

    def accepted(self) -> list[dict[str, Any]]:
        return [
            record
            for record in self.history()
            if bool(record.get("evaluation", {}).get("accepted", False))
        ]

    def rejected(self) -> list[dict[str, Any]]:
        return [
            record
            for record in self.history()
            if not bool(record.get("evaluation", {}).get("accepted", False))
        ]

    def best(self, limit: int = 10) -> list[dict[str, Any]]:
        return self.store.best(limit=limit)

    def summarize(self) -> EvolutionMemorySummary:
        records = self.history()
        accepted = self.accepted()
        rejected = self.rejected()

        scores = [
            float(record.get("evaluation", {}).get("score", 0.0))
            for record in records
        ]

        successful_patterns: list[str] = []
        failed_patterns: list[str] = []

        for record in accepted:
            evaluation = record.get("evaluation", {})
            proposal = record.get("proposal", {})

            category = proposal.get("category", "unknown")
            target = proposal.get("target", "unknown")
            score = float(evaluation.get("score", 0.0))

            successful_patterns.append(
                f"accepted: category={category}, "
                f"target={target}, score={score:.3f}"
            )

        for record in rejected:
            evaluation = record.get("evaluation", {})
            proposal = record.get("proposal", {})

            category = proposal.get("category", "unknown")
            target = proposal.get("target", "unknown")
            reason = evaluation.get("reason", "unknown")

            failed_patterns.append(
                f"rejected: category={category}, "
                f"target={target}, reason={reason}"
            )

        return EvolutionMemorySummary(
            total=len(records),
            accepted=len(accepted),
            rejected=len(rejected),
            best_score=max(scores, default=0.0),
            successful_patterns=successful_patterns,
            failed_patterns=failed_patterns,
        )

    def build_context(self, limit: int = 10) -> dict[str, Any]:
        summary = self.summarize()

        return {
            "evolution_memory": {
                "total": summary.total,
                "accepted": summary.accepted,
                "rejected": summary.rejected,
                "best_score": summary.best_score,
                "successful_patterns": summary.successful_patterns[-limit:],
                "failed_patterns": summary.failed_patterns[-limit:],
            }
        }
