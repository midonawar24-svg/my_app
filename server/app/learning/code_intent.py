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

    It maps Arabic/English user wording to discovered evolution domains.
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
        text = (
            text.replace("أ", "ا")
            .replace("إ", "ا")
            .replace("آ", "ا")
        )
        return text

    def _domain_terms(self, domain_id: str, domain: Any) -> tuple[str, ...]:
        terms = [
            domain.name,
            *getattr(domain, "aliases", ()),
            domain_id.rsplit(".", 1)[-1],
        ]

        return tuple(
            dict.fromkeys(
                self._normalize(term)
                for term in terms
                if term and self._normalize(term)
            )
        )

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

        # Exact domain IDs remain the strongest signal.
        exact_matches = [
            domain_id
            for domain_id in domains
            if self._normalize(domain_id) in text
        ]

        if exact_matches:
            domain_id = max(
                exact_matches,
                key=lambda value: (
                    len(value),
                    len(value.split(".")),
                ),
            )

            return CodeIntent(
                is_code_request=True,
                domain_id=domain_id,
                confidence=1.0,
                reason="Exact domain ID matched",
            )

        # Score discovered domain names, aliases, and filesystem branches.
        candidates: list[tuple[int, int, int, str]] = []

        for domain_id, domain in domains.items():
            depth = len(domain_id.split("."))

            for term in self._domain_terms(domain_id, domain):
                if term not in text:
                    continue

                candidates.append(
                    (
                        len(term),
                        depth,
                        1 if term == self._normalize(domain.name) else 0,
                        domain_id,
                    )
                )

        if candidates:
            _, _, _, domain_id = max(candidates)

            return CodeIntent(
                is_code_request=True,
                domain_id=domain_id,
                confidence=0.9,
                reason="Natural-language domain alias matched",
            )

        return CodeIntent(
            is_code_request=True,
            domain_id=None,
            confidence=0.5,
            reason="Code request detected but domain is ambiguous",
        )
