from typing import Any

from app.providers.factory import get_provider
from app.services.config import get_ai_provider_name


class AIService:
    def __init__(self, provider_name: str | None = None):
        selected_provider = provider_name or get_ai_provider_name()
        self.provider_name = selected_provider
        self.provider = get_provider(selected_provider)

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
