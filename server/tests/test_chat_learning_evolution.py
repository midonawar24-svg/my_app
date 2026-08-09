import asyncio

from app.api.v1 import chat


class FakeGateway:
    async def ask(
        self,
        message,
        conversation_id=None,
        context=None,
    ):
        return "Teacher reply"


def test_chat_learning_evolution_path(monkeypatch):
    calls = []

    class FakeFlow:
        def __init__(self, learning_pipeline):
            calls.append(("init", learning_pipeline))

        async def process(self, message, **kwargs):
            calls.append(("process", message, kwargs))

    async def fake_ask(
        self,
        message,
        conversation_id=None,
        context=None,
    ):
        return "Teacher reply"

    monkeypatch.setattr(chat, "TeacherGateway", FakeGateway)
    monkeypatch.setattr(chat, "LearningEvolutionFlow", FakeFlow)

    class Request:
        message = "Teach me a successful pattern"
        conversation_id = "chat-flow-test"
        conversationId = None
        context = {"test": True}
        should_remember = True
        confidence = 0.95
        memory_type = "knowledge"

    result = asyncio.run(chat.chat(Request()))

    assert result.reply == "Teacher reply"

    assert calls
    assert calls[0][0] == "init"

    process_call = calls[1]
    assert process_call[0] == "process"
    assert process_call[1] == "Teach me a successful pattern"
    assert process_call[2]["conversation_id"] == "chat-flow-test"
    assert process_call[2]["should_remember"] is True
    assert process_call[2]["confidence"] == 0.95


if __name__ == "__main__":
    test_chat_learning_evolution_path(
        type("MonkeyPatch", (), {})()
    )
