import asyncio

import pytest

from app.services.teacher_gateway import TeacherGateway


class MockAIService:
    def __init__(self, reply="Teacher reply"):
        self.reply = reply
        self.calls = []

    async def generate(self, message, conversation_id=None, context=None):
        self.calls.append({
            "message": message,
            "conversation_id": conversation_id,
            "context": context,
        })
        return self.reply


def test_teacher_gateway_forwards_request():
    service = MockAIService("Hello from teacher")
    gateway = TeacherGateway(service)

    reply = asyncio.run(
        gateway.ask(
            "  HELLO TEACHER  ",
            conversation_id="conv-1",
            context={"topic": "AI"},
        )
    )

    assert reply == "Hello from teacher"
    assert service.calls == [{
        "message": "HELLO TEACHER",
        "conversation_id": "conv-1",
        "context": {"topic": "AI"},
    }]


def test_teacher_gateway_rejects_empty_message():
    service = MockAIService()
    gateway = TeacherGateway(service)

    with pytest.raises(ValueError, match="Teacher message cannot be empty"):
        asyncio.run(gateway.ask("   "))


def test_teacher_gateway_rejects_empty_reply():
    service = MockAIService("   ")
    gateway = TeacherGateway(service)

    with pytest.raises(
        RuntimeError,
        match="Teacher returned an empty response",
    ):
        asyncio.run(gateway.ask("HELLO"))


def test_teacher_gateway_strips_reply():
    service = MockAIService("   Teacher response   ")
    gateway = TeacherGateway(service)

    reply = asyncio.run(gateway.ask("HELLO"))

    assert reply == "Teacher response"
