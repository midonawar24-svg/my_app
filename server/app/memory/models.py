from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MemoryWriteRequest:
    content: str
    conversation_id: str
    memory_type: str
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class MemoryWriteResult:
    accepted: bool
    memory_id: str | None = None
    reason: str = ""
