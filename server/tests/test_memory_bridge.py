from app.learning.memory_bridge import MemoryBridge
from app.learning.models import LearningCandidate


def make_candidate(**overrides):
    data = {
        "content": "The AI Core OS learned this fact.",
        "source": "teacher",
        "conversation_id": "bridge-test",
        "confidence": 0.95,
        "category": "knowledge",
        "should_remember": True,
        "metadata": {"test": True},
    }
    data.update(overrides)
    return LearningCandidate(**data)


def test_bridge_builds_memory_write_request():
    request = MemoryBridge().build_write_request(make_candidate())

    assert request.content == "The AI Core OS learned this fact."
    assert request.conversation_id == "bridge-test"
    assert request.memory_type == "knowledge"
    assert request.metadata["source"] == "teacher"
    assert request.metadata["confidence"] == 0.95
    assert request.metadata["category"] == "knowledge"
    assert request.metadata["test"] is True


def test_bridge_rejects_memory_not_approved():
    candidate = make_candidate(should_remember=False)

    try:
        MemoryBridge().build_write_request(candidate)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Learning candidate is not approved for memory"


def test_bridge_rejects_empty_content():
    candidate = make_candidate(content="   ")

    try:
        MemoryBridge().build_write_request(candidate)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Cannot bridge empty learning content"
