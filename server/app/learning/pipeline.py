from typing import Any

from app.learning.engine import LearningEngine
from app.learning.memory_sink import LearningMemorySink


class LearningPipeline:
    """Coordinates teacher learning, validation, and memory persistence."""

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
    ):
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

        return await self.memory_sink.persist(candidate)
