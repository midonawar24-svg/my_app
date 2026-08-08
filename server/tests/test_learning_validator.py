from app.learning.models import LearningCandidate
from app.learning.validator import LearningValidator


def candidate(
    *,
    confidence=0.9,
    should_remember=True,
    content="A valid learned fact.",
):
    return LearningCandidate(
        content=content,
        source="teacher",
        conversation_id="validation-test",
        confidence=confidence,
        category="knowledge",
        should_remember=should_remember,
    )


def test_validator_accepts_valid_candidate():
    result = LearningValidator().validate(candidate())

    assert result.accepted is True
    assert result.reason == "accepted"


def test_validator_rejects_when_memory_not_requested():
    result = LearningValidator().validate(
        candidate(should_remember=False)
    )

    assert result.accepted is False
    assert result.reason == "memory_not_requested"


def test_validator_rejects_low_confidence():
    result = LearningValidator().validate(
        candidate(confidence=0.69)
    )

    assert result.accepted is False
    assert result.reason == "confidence_too_low"


def test_validator_rejects_empty_content():
    result = LearningValidator().validate(
        candidate(content="   ")
    )

    assert result.accepted is False
    assert result.reason == "empty_content"
