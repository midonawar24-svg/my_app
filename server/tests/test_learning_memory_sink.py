import asyncio

from app.learning.memory_sink import LearningMemorySink
from app.learning.models import LearningCandidate


class FakeMemoryStore:
    def __init__(self):
        self.saved = []

    async def remember(
        self,
        content,
        memory_type,
        conversation_id=None,
        metadata=None,
    ):
        self.saved.append(
            {
                "content": content,
                "memory_type": memory_type,
                "conversation_id": conversation_id,
                "metadata": metadata,
            }
        )


def make_candidate(
    *,
    confidence=0.9,
    should_remember=True,
):
    return LearningCandidate(
        content="Learned fact",
        source="teacher",
        conversation_id="memory-test",
        confidence=confidence,
        category="knowledge",
        should_remember=should_remember,
    )


def test_accepted_candidate_reaches_memory():
    memory = FakeMemoryStore()
    sink = LearningMemorySink(memory)

    stored = asyncio.run(
        sink.store(make_candidate())
    )

    assert stored is True
    assert len(memory.saved) == 1
    assert memory.saved[0]["content"] == "Learned fact"
    assert memory.saved[0]["memory_type"] == "knowledge"
    assert memory.saved[0]["conversation_id"] == "memory-test"
    assert memory.saved[0]["metadata"]["source"] == "teacher"
    assert memory.saved[0]["metadata"]["confidence"] == 0.9


def test_rejected_candidate_never_reaches_memory():
    memory = FakeMemoryStore()
    sink = LearningMemorySink(memory)

    stored = asyncio.run(
        sink.store(
            make_candidate(
                confidence=0.5,
            )
        )
    )

    assert stored is False
    assert memory.saved == []


def test_memory_not_requested_never_reaches_memory():
    memory = FakeMemoryStore()
    sink = LearningMemorySink(memory)

    stored = asyncio.run(
        sink.store(
            make_candidate(
                should_remember=False,
            )
        )
    )

    assert stored is False
    assert memory.saved == []
