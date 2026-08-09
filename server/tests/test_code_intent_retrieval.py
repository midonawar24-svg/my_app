from pathlib import Path

from app.learning.code_intent import CodeIntentResolver
from app.learning.code_retriever import CodeRetriever


def create_domain(root: Path, domain: str) -> None:
    path = root / "app" / "memory" / "interests" / domain
    path.mkdir(parents=True)
    (path / "__init__.py").write_text(
        f"# {domain}\n",
        encoding="utf-8",
    )


def resolve_and_retrieve(root: Path, message: str):
    retriever = CodeRetriever(root)
    intent = CodeIntentResolver(retriever).resolve(message)

    assert intent.is_code_request is True
    assert intent.domain_id is not None

    return intent, retriever.retrieve(intent.domain_id)


def test_arabic_dynamic_domain_retrieval(tmp_path):
    create_domain(tmp_path, "weather")

    intent, result = resolve_and_retrieve(
        tmp_path,
        "هات كود weather",
    )

    assert intent.domain_id == "memory.interests.weather"
    assert (
        "app/memory/interests/weather/__init__.py"
        in result.files
    )


def test_english_dynamic_domain_retrieval(tmp_path):
    create_domain(tmp_path, "weather")

    intent, result = resolve_and_retrieve(
        tmp_path,
        "show me the code for weather",
    )

    assert intent.domain_id == "memory.interests.weather"
    assert (
        "app/memory/interests/weather/__init__.py"
        in result.files
    )


def test_arabic_memory_retrieval():
    intent, result = resolve_and_retrieve(
        Path("."),
        "هات ملفات memory interests",
    )

    assert intent.domain_id == "memory"
    assert result.files


def test_personal_memory_is_protected():
    intent, result = resolve_and_retrieve(
        Path("."),
        "هات ملفات memory",
    )

    assert "memory.personal" in result.protected_domains

    assert all(
        "memory.personal" not in path
        for path in result.files
    )
