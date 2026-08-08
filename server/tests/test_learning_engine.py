import pytest

from app.learning.engine import LearningEngine
from app.learning.models import LearningCandidate


def test_build_learning_candidate():
    engine = LearningEngine()

    candidate = engine.build_candidate(
        "  Python is a programming language.  ",
        source="teacher",
        conversation_id="learning-1",
        confidence=0.95,
        category="knowledge",
        should_remember=True,
    )

    assert isinstance(candidate, LearningCandidate)
    assert candidate.content == "Python is a programming language."
    assert candidate.source == "teacher"
    assert candidate.conversation_id == "learning-1"
    assert candidate.confidence == 0.95
    assert candidate.category == "knowledge"
    assert candidate.should_remember is True


def test_learning_content_cannot_be_empty():
    engine = LearningEngine()

    with pytest.raises(ValueError, match="Learning content cannot be empty"):
        engine.build_candidate("   ")


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_confidence_must_be_between_zero_and_one(confidence):
    engine = LearningEngine()

    with pytest.raises(
        ValueError,
        match="Learning confidence must be between 0 and 1",
    ):
        engine.build_candidate("FACT", confidence=confidence)


def test_learning_engine_learns_from_teacher():
    import asyncio

    class FakeTeacherGateway:
        async def ask(
            self,
            message,
            conversation_id=None,
            context=None,
        ):
            assert message == "TEACH ME"
            assert conversation_id == "conversation-1"
            assert context == {"topic": "python"}

            return "Python uses indentation to define code blocks."

    from app.learning.engine import LearningEngine

    engine = LearningEngine()

    candidate = asyncio.run(
        engine.learn_from_teacher(
            FakeTeacherGateway(),
            "TEACH ME",
            conversation_id="conversation-1",
            context={"topic": "python"},
            confidence=0.9,
            category="knowledge",
            should_remember=True,
        )
    )

    assert candidate.content == (
        "Python uses indentation to define code blocks."
    )
    assert candidate.source == "teacher"
    assert candidate.conversation_id == "conversation-1"
    assert candidate.confidence == 0.9
    assert candidate.category == "knowledge"
    assert candidate.should_remember is True
