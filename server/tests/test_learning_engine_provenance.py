from app.learning.engine import LearningEngine


def test_learning_candidate_adds_provenance_metadata():
    candidate = LearningEngine().build_candidate(
        "  Learned behavior  ",
        source="teacher",
        category="knowledge",
        confidence=0.95,
        should_remember=True,
    )

    assert candidate.content == "Learned behavior"
    assert candidate.source == "teacher"
    assert candidate.category == "knowledge"
    assert candidate.metadata["learning_source"] == "teacher"
    assert candidate.metadata["learning_category"] == "knowledge"
    assert candidate.metadata["normalized"] is True


def test_existing_metadata_is_preserved():
    candidate = LearningEngine().build_candidate(
        "Learned behavior",
        source="teacher",
        metadata={"lesson_id": "lesson-1"},
    )

    assert candidate.metadata["lesson_id"] == "lesson-1"
    assert candidate.metadata["learning_source"] == "teacher"
    assert candidate.metadata["normalized"] is True
