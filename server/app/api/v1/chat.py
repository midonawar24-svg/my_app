from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.teacher_gateway import TeacherGateway
from app.learning.memory_sink import LearningMemorySink
from app.learning.pipeline import LearningPipeline
from app.memory.in_memory_gateway import InMemoryMemoryGateway


router = APIRouter()

memory_gateway = InMemoryMemoryGateway()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    conversationId: str | None = None
    context: dict[str, Any] | None = None
    should_remember: bool = False
    confidence: float = 0.0
    memory_type: str = "knowledge"


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    conversation_id = request.conversation_id or request.conversationId

    gateway = TeacherGateway()

    reply = await gateway.ask(
        message=request.message,
        conversation_id=conversation_id,
        context=request.context,
    )

    if request.should_remember:
        try:
            pipeline = LearningPipeline(
                gateway,
                LearningMemorySink(memory_gateway),
            )

            await pipeline.learn(
                request.message,
                conversation_id=conversation_id,
                context=request.context,
                source="teacher",
                confidence=request.confidence,
                category=request.memory_type,
                should_remember=True,
                reply=reply,
            )
        except Exception:
            # Learning persistence must never break the primary chat response.
            pass

    return ChatResponse(
        reply=reply,
        conversation_id=conversation_id,
    )
