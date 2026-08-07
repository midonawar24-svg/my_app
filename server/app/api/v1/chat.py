from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.ai_service import AIService


router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    conversationId: str | None = None
    context: dict[str, Any] | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    conversation_id = request.conversation_id or request.conversationId

    service = AIService(provider_name="echo")

    reply = await service.generate(
        message=request.message,
        conversation_id=conversation_id,
        context=request.context,
    )

    return ChatResponse(
        reply=reply,
        conversation_id=conversation_id,
    )
