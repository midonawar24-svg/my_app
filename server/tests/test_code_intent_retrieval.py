from pathlib import Path

from app.learning.code_intent import CodeIntentResolver
from app.learning.code_retriever import CodeRetriever


def resolve_and_retrieve(message: str):
    retriever = CodeRetriever(Path("."))
    intent = CodeIntentResolver(retriever).resolve(message)

    assert intent.is_code_request is True
    assert intent.domain_id is not None

    return intent, retriever.retrieve(intent.domain_id)


def test_arabic_sports_retrieval():
    intent, result = resolve_and_retrieve("هات كود sports")

    assert intent.domain_id == "memory.interests.sports"
    assert "app/memory/interests/sports/__init__.py" in result.files


def test_english_football_retrieval():
    intent, result = resolve_and_retrieve(
        "show me the code for football"
    )

    assert intent.domain_id == "memory.interests.sports.football"
    assert (
        "app/memory/interests/sports/football/__init__.py"
        in result.files
    )


def test_arabic_memory_retrieval():
    intent, result = resolve_and_retrieve(
        "هات ملفات memory interests"
    )

    assert intent.domain_id == "memory"
    assert result.files


def test_personal_memory_is_protected():
    intent, result = resolve_and_retrieve(
        "هات ملفات memory"
    )

    assert "memory.personal" in result.protected_domains

    assert all(
        "memory.personal" not in path
        for path in result.files
    )
