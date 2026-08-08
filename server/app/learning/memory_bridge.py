from dataclasses import dataclass
from typing import Any

from app.learning.models import LearningCandidate


@dataclass(frozen=True)
class MemoryWriteRequest:
    content: str
    conversation_id: str | None
    memory_type: str
    metadata: dict[str, Any]


class MemoryBridge:
    """
    Bridge between the learning pipeline and AI Core OS memory.

    The bridge prepares an accepted learning candidate for the
    real MemoryEngine. It does not own storage and does not duplicate
    the MemoryEngine implementation.
    """

    def build_write_request(
        self,
        candidate: LearningCandidate,
    ) -> MemoryWriteRequest:
        if not candidate.content.strip():
            raise ValueError("Cannot bridge empty learning content")

        if not candidate.should_remember:
            raise ValueError("Learning candidate is not approved for memory")

        metadata = dict(candidate.metadata or {})

        metadata.setdefault("source", candidate.source)
        metadata.setdefault("confidence", candidate.confidence)
        metadata.setdefault("category", candidate.category)
        metadata.setdefault("learning_pipeline", "teacher")

        return MemoryWriteRequest(
            content=candidate.content.strip(),
            conversation_id=candidate.conversation_id,
            memory_type=candidate.category,
            metadata=metadata,
        )
