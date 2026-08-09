import asyncio

from app.api.v1 import chat


def test_chat_learning_configuration_uses_memory_gateway():
    async def run():
        await chat.memory_gateway.remember(
            content="Integration fact",
            conversation_id="chat-test",
            memory_type="knowledge",
            metadata={"source": "teacher"},
        )

        assert len(chat.memory_gateway.saved) >= 1

        saved = chat.memory_gateway.saved[-1]
        assert saved["content"] == "Integration fact"
        assert saved["conversation_id"] == "chat-test"
        assert saved["memory_type"] == "knowledge"
        assert saved["metadata"]["source"] == "teacher"

    asyncio.run(run())


def test_chat_code_retrieval_context(monkeypatch):
    from pathlib import Path

    from app.api.v1 import chat

    captured = {}

    class FakeGateway:
        async def ask(
            self,
            message,
            conversation_id=None,
            context=None,
        ):
            captured["message"] = message
            captured["conversation_id"] = conversation_id
            captured["context"] = context
            return "Code reply"

    monkeypatch.setattr(chat, "TeacherGateway", FakeGateway)

    class Request:
        message = "هات كود sports"
        conversation_id = "code-chat-test"
        conversationId = None
        context = None
        should_remember = False
        confidence = 0.0
        memory_type = "knowledge"

    result = asyncio.run(chat.chat(Request()))

    assert result.reply == "Code reply"

    code_context = captured["context"]["code_retrieval"]

    assert code_context["domain_id"] == "memory.interests.sports"
    assert (
        "app/memory/interests/sports/__init__.py"
        in code_context["files"]
    )
