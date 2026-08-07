from typing import Any
from app.providers.factory import get_provider

class AIService:
    def __init__(self, provider_name: str = "echo"):
        self.provider = get_provider(provider_name)

    async def generate(
        self,
        message: str,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        return await self.provider.generate(
            message=message,
            conversation_id=conversation_id,
            context=context,
        )
