from typing import Any
from .base import AIProvider

class EchoProvider(AIProvider):
    async def generate(
        self,
        message: str,
        conversation_id: str = "",
        context: dict[str, Any] | None = None,
    ) -> str:
        return f"Echo: {message}"
