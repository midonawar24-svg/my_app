from typing import Any

from app.memory.models import MemoryWriteRequest, MemoryWriteResult


class MemoryGateway:
    """
    Contract boundary between backend learning and the app memory system.

    This layer does not know how Flutter/Hive stores memory.
    It only defines the write operation that the transport layer will use.
    """

    async def remember(
        self,
        content: str,
        conversation_id: str,
        memory_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryWriteResult:
        raise NotImplementedError
