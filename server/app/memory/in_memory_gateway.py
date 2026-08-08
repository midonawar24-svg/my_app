from typing import Any

from app.memory.gateway import MemoryGateway
from app.memory.models import MemoryWriteResult


class InMemoryMemoryGateway(MemoryGateway):
    """Simple backend memory gateway implementation."""

    def __init__(self):
        self.saved: list[dict[str, Any]] = []

    async def remember(
        self,
        content: str,
        conversation_id: str,
        memory_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryWriteResult:
        memory_id = f"memory-{len(self.saved) + 1}"

        self.saved.append(
            {
                "id": memory_id,
                "content": content,
                "conversation_id": conversation_id,
                "memory_type": memory_type,
                "metadata": dict(metadata or {}),
            }
        )

        return MemoryWriteResult(
            accepted=True,
            memory_id=memory_id,
            reason="saved",
        )
