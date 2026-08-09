from pathlib import Path

from app.learning.code_intent import CodeIntentResolver
from app.learning.code_retriever import CodeRetriever


def resolver():
    return CodeIntentResolver(CodeRetriever(Path(".")))


def test_arabic_sports_command():
    result = resolver().resolve("هات كود sports")

    assert result.is_code_request is True
    assert result.domain_id == "memory.interests.sports"


def test_english_football_command():
    result = resolver().resolve("show me the code for football")

    assert result.is_code_request is True
    assert result.domain_id == "memory.interests.sports.football"


def test_arabic_memory_command():
    result = resolver().resolve("هات ملفات memory interests")

    assert result.is_code_request is True
    assert result.domain_id == "memory"


def test_non_code_message():
    result = resolver().resolve("ايه اخبار النظام؟")

    assert result.is_code_request is False
    assert result.domain_id is None


def test_english_non_code_message():
    result = resolver().resolve("how is the system doing?")

    assert result.is_code_request is False
    assert result.domain_id is None
