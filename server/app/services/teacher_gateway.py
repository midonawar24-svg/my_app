from typing import Any

from app.services.ai_service import AIService


class TeacherGateway:
    """
    Gateway between AI Core OS and the external AI teacher.

    This layer intentionally stays separate from the provider itself so
    learning, memory, validation, and decision logic can be added later.
    """

    def __init__(self, ai_service: AIService | None = None):
        self.ai_service = ai_service or AIService()

    async def ask(
        self,
        message: str,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        text = message.strip()

        if not text:
            raise ValueError("Teacher message cannot be empty")

        reply = await self.ai_service.generate(
            message=text,
            conversation_id=conversation_id,
            context=context,
        )

        if not isinstance(reply, str) or not reply.strip():
            raise RuntimeError("Teacher returned an empty response")

        return reply.strip()
