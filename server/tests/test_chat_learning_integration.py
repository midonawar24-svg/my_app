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
