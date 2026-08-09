from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvolutionProposal:
    proposal_id: str
    title: str
    description: str
    category: str
    target: str
    expected_gain: float = 0.0
    confidence: float = 0.0
    risk: float = 0.0
    evidence: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvolutionEvaluation:
    proposal_id: str
    accepted: bool
    score: float
    reason: str
    evidence: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
