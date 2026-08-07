from typing import Any
from .base import AIProvider

class FakeProvider(AIProvider):
    """
    Provider وهمي للاختبار بدون موديل حقيقي.
    """

    async def generate(
        self,
        message: str,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        text = message.strip()

        if not text:
            return "Fake: رسالة فارغة!"

        return f"Fake AI: استقبلت '{text}'"
