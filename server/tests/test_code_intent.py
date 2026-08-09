from pathlib import Path

from app.learning.code_intent import CodeIntentResolver
from app.learning.code_retriever import CodeRetriever


def resolver(root: Path):
    return CodeIntentResolver(CodeRetriever(root))


def create_domain(root: Path, domain: str) -> None:
    path = root / "app" / "memory" / "interests" / domain
    path.mkdir(parents=True)
    (path / "__init__.py").write_text(
        f"# {domain}\n",
        encoding="utf-8",
    )


def test_arabic_dynamic_domain_command(tmp_path):
    create_domain(tmp_path, "weather")

    result = resolver(tmp_path).resolve("هات كود weather")

    assert result.is_code_request is True
    assert result.domain_id == "memory.interests.weather"


def test_english_dynamic_domain_command(tmp_path):
    create_domain(tmp_path, "weather")

    result = resolver(tmp_path).resolve(
        "show me the code for weather"
    )

    assert result.is_code_request is True
    assert result.domain_id == "memory.interests.weather"


def test_arabic_memory_command():
    result = resolver(Path(".")).resolve(
        "هات ملفات memory interests"
    )

    assert result.is_code_request is True
    assert result.domain_id == "memory"


def test_non_code_message():
    result = resolver(Path(".")).resolve(
        "ايه اخبار النظام؟"
    )

    assert result.is_code_request is False
    assert result.domain_id is None


def test_english_non_code_message():
    result = resolver(Path(".")).resolve(
        "how is the system doing?"
    )

    assert result.is_code_request is False
    assert result.domain_id is None
