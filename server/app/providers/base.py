from abc import ABC, abstractmethod
from typing import Any
class AIProvider(ABC):
    @abstractmethod
    async def generate(self, message: str, conversation_id: str = "", context: dict[str, Any] | None = None) -> str: pass
