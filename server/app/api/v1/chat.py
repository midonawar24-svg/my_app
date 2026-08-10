from pathlib import Path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.teacher_gateway import TeacherGateway
from app.learning.memory_sink import LearningMemorySink
from app.learning.learning_evolution_flow import LearningEvolutionFlow
from app.learning.code_intent import CodeIntentResolver
from app.learning.code_retriever import CodeRetriever
from app.learning.pipeline import LearningPipeline
from app.memory.in_memory_gateway import InMemoryMemoryGateway


router = APIRouter()

memory_gateway = InMemoryMemoryGateway()

project_root = Path(__file__).resolve().parents[3]
code_retriever = CodeRetriever(project_root)
code_intent_resolver = CodeIntentResolver(code_retriever)


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

    context = dict(request.context or {})

    code_intent = code_intent_resolver.resolve(request.message)

    if code_intent.is_code_request and code_intent.domain_id:
        retrieval = code_retriever.retrieve(code_intent.domain_id)

        context["code_retrieval"] = {
            "domain_id": retrieval.domain_id,
            "domain_ids": list(retrieval.domain_ids),
            "files": list(retrieval.files),
            "protected_domains": list(retrieval.protected_domains),
            "confidence": code_intent.confidence,
        }

    gateway = TeacherGateway()

    reply = await gateway.ask(
        message=request.message,
        conversation_id=conversation_id,
        context=context or None,
    )

    if request.should_remember:
        try:
            pipeline = LearningPipeline(
                gateway,
                LearningMemorySink(memory_gateway),
            )

            flow = LearningEvolutionFlow(
                learning_pipeline=pipeline,
            )

            await flow.process(
                request.message,
                conversation_id=conversation_id,
                context=context or None,
                source="teacher",
                confidence=request.confidence,
                category=request.memory_type,
                should_remember=True,
                reply=reply,
                expected_gain=0.80,
                risk=0.20,
            )
        except Exception:
            # Learning persistence must never break the primary chat response.
            pass

    return ChatResponse(
        reply=reply,
        conversation_id=conversation_id,
    )
