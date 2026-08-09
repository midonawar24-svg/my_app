import hashlib
from typing import Any

from app.learning.models import LearningCandidate


class LearningEngine:
    """
    Converts teacher responses into learning candidates.

    This layer does not write to memory.
    Validation and memory integration come later.
    """

    async def learn_from_teacher(
        self,
        teacher_gateway,
        message: str,
        *,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
        source: str = "teacher",
        confidence: float = 0.0,
        category: str = "unknown",
        should_remember: bool = False,
        metadata: dict[str, Any] | None = None,
        reply: str | None = None,
    ) -> LearningCandidate:
        if reply is None:
            reply = await teacher_gateway.ask(
                message=message,
                conversation_id=conversation_id,
                context=context,
            )

        return self.build_candidate(
            reply,
            source=source,
            conversation_id=conversation_id,
            confidence=confidence,
            category=category,
            should_remember=should_remember,
            metadata=metadata,
        )

    def build_candidate(
        self,
        content: str,
        *,
        source: str = "teacher",
        conversation_id: str | None = None,
        confidence: float = 0.0,
        category: str = "unknown",
        should_remember: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> LearningCandidate:
        text = content.strip()

        if not text:
            raise ValueError("Learning content cannot be empty")

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Learning confidence must be between 0 and 1"
            )

        normalized_source = source.strip() or "teacher"
        normalized_category = category.strip() or "unknown"

        candidate_metadata = dict(metadata or {})
        candidate_metadata.setdefault("learning_source", normalized_source)
        candidate_metadata.setdefault("learning_category", normalized_category)
        candidate_metadata.setdefault("normalized", True)

        fingerprint_input = (
            f"{normalized_source}\n"
            f"{normalized_category}\n"
            f"{text}"
        )
        fingerprint = hashlib.sha256(
            fingerprint_input.encode("utf-8")
        ).hexdigest()

        candidate_metadata.setdefault("fingerprint", fingerprint)

        return LearningCandidate(
            content=text,
            source=normalized_source,
            conversation_id=conversation_id,
            confidence=confidence,
            category=normalized_category,
            should_remember=should_remember,
            metadata=candidate_metadata,
        )
