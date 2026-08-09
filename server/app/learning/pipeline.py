from dataclasses import dataclass
from typing import Any

from app.learning.engine import LearningEngine
from app.learning.memory_sink import LearningMemorySink
from app.learning.models import LearningCandidate
from app.memory.models import MemoryWriteResult


@dataclass(frozen=True)
class LearningPipelineResult:
    accepted: bool
    memory_id: str | None
    reason: str
    candidate: LearningCandidate


class LearningPipeline:
    """
    Coordinates teacher learning, validation, memory persistence,
    and exposes the accepted learning candidate to the evolution layer.

    The teacher supplies knowledge.
    The learning layer owns persistence and downstream evolution.
    """

    def __init__(
        self,
        teacher_gateway,
        memory_sink: LearningMemorySink,
        learning_engine: LearningEngine | None = None,
    ):
        self.teacher_gateway = teacher_gateway
        self.memory_sink = memory_sink
        self.learning_engine = learning_engine or LearningEngine()

    async def learn(
        self,
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
    ) -> LearningPipelineResult:
        candidate = await self.learning_engine.learn_from_teacher(
            self.teacher_gateway,
            message,
            conversation_id=conversation_id,
            context=context,
            source=source,
            confidence=confidence,
            category=category,
            should_remember=should_remember,
            metadata=metadata,
            reply=reply,
        )

        result = await self.memory_sink.persist(candidate)

        return LearningPipelineResult(
            accepted=result.accepted,
            memory_id=result.memory_id,
            reason=result.reason,
            candidate=candidate,
        )
