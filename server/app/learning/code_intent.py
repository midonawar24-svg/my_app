from dataclasses import dataclass
import re
from typing import Any

from app.learning.code_retriever import CodeRetriever


@dataclass(frozen=True)
class CodeIntent:
    is_code_request: bool
    domain_id: str | None
    confidence: float
    reason: str


class CodeIntentResolver:
    """
    Read-only resolver for natural-language code retrieval requests.

    It maps Arabic/English user wording to known evolution domains.
    It never edits or executes project code.
    """

    CODE_PATTERNS = (
        r"\bcode\b",
        r"\bcodes\b",
        r"\bfile\b",
        r"\bfiles\b",
        r"\bsource\b",
        r"\bimplementation\b",
        r"كود",
        r"اكواد",
        r"أكواد",
        r"ملف",
        r"ملفات",
        r"كودات",
        r"مصدر",
    )

    ACTION_PATTERNS = (
        r"\bget\b",
        r"\bfetch\b",
        r"\bshow\b",
        r"\bretrieve\b",
        r"\bbring\b",
        r"\bfind\b",
        r"\bgive\b",
        r"هات",
        r"هاتلي",
        r"هات لي",
        r"جيب",
        r"جيبي",
        r"اعرض",
        r"أعرض",
        r"جيبلي",
    )

    def __init__(self, retriever: CodeRetriever):
        self.retriever = retriever

    def _all_domains(self) -> dict[str, Any]:
        return self.retriever._build_domains()

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        return text

    def resolve(self, message: str) -> CodeIntent:
        text = self._normalize(message)

        has_code = any(
            re.search(pattern, text)
            for pattern in self.CODE_PATTERNS
        )

        has_action = any(
            re.search(pattern, text)
            for pattern in self.ACTION_PATTERNS
        )

        if not has_code or not has_action:
            return CodeIntent(
                is_code_request=False,
                domain_id=None,
                confidence=0.0,
                reason="No code-retrieval intent detected",
            )

        domains = self._all_domains()

        # Prefer exact domain IDs first.
        for domain_id in sorted(
            domains,
            key=len,
            reverse=True,
        ):
            if self._normalize(domain_id) in text:
                return CodeIntent(
                    is_code_request=True,
                    domain_id=domain_id,
                    confidence=1.0,
                    reason="Exact domain ID matched",
                )

        # Then match domain names and filesystem branch names.
        for domain_id, domain in sorted(
            domains.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            name = self._normalize(domain.name)

            if name and name in text:
                return CodeIntent(
                    is_code_request=True,
                    domain_id=domain_id,
                    confidence=0.9,
                    reason="Domain name matched",
                )

            branch = domain_id.rsplit(".", 1)[-1]
            branch = self._normalize(branch)

            if branch and branch in text:
                return CodeIntent(
                    is_code_request=True,
                    domain_id=domain_id,
                    confidence=0.85,
                    reason="Domain branch matched",
                )

        return CodeIntent(
            is_code_request=True,
            domain_id=None,
            confidence=0.5,
            reason="Code request detected but domain is ambiguous",
        )
