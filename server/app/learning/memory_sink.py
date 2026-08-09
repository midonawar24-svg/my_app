from app.learning.models import LearningCandidate
from app.learning.validator import LearningValidator
from app.memory.gateway import MemoryGateway


class LearningMemorySink:
    """
    Sends validated learning candidates to the memory gateway.

    Duplicate fingerprints are rejected within this sink instance.
    """

    def __init__(
        self,
        memory_gateway: MemoryGateway,
        validator: LearningValidator | None = None,
    ):
        self.memory_gateway = memory_gateway
        self.validator = validator or LearningValidator()
        self._fingerprints: set[str] = set()

    async def store(self, candidate: LearningCandidate):
        result = await self.persist(candidate)

        if hasattr(result, "accepted"):
            return result.accepted

        return bool(result)

    async def persist(self, candidate: LearningCandidate):
        validation = self.validator.validate(candidate)

        if not validation.accepted:
            return validation

        metadata = dict(candidate.metadata or {})
        metadata.setdefault("source", candidate.source)
        metadata.setdefault("confidence", candidate.confidence)

        fingerprint = metadata.get("fingerprint")

        if fingerprint and fingerprint in self._fingerprints:
            from app.memory.models import MemoryWriteResult

            return MemoryWriteResult(
                accepted=False,
                reason="duplicate",
            )

        result = await self.memory_gateway.remember(
            content=candidate.content,
            conversation_id=candidate.conversation_id or "",
            memory_type=candidate.category,
            metadata=metadata,
        )

        if result is None:
            from app.memory.models import MemoryWriteResult

            if fingerprint:
                self._fingerprints.add(fingerprint)

            return MemoryWriteResult(
                accepted=True,
                reason="saved",
            )

        if getattr(result, "accepted", False) and fingerprint:
            self._fingerprints.add(fingerprint)

        return result
