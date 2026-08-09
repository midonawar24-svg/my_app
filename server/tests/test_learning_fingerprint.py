from app.learning.engine import LearningEngine


def test_same_learning_content_gets_same_fingerprint():
    engine = LearningEngine()

    first = engine.build_candidate(
        "Python uses indentation.",
        source="teacher",
        category="knowledge",
    )

    second = engine.build_candidate(
        "  Python uses indentation.  ",
        source="teacher",
        category="knowledge",
    )

    assert first.metadata["fingerprint"] == second.metadata["fingerprint"]


def test_different_learning_content_gets_different_fingerprint():
    engine = LearningEngine()

    first = engine.build_candidate(
        "Python uses indentation.",
        source="teacher",
        category="knowledge",
    )

    second = engine.build_candidate(
        "Python uses braces.",
        source="teacher",
        category="knowledge",
    )

    assert first.metadata["fingerprint"] != second.metadata["fingerprint"]
