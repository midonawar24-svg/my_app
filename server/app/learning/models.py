from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LearningCandidate:
    content: str
    source: str
    conversation_id: str | None = None
    confidence: float = 0.0
    category: str = "unknown"
    should_remember: bool = False
    metadata: dict[str, Any] | None = None
