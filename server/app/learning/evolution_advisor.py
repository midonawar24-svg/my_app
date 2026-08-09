import json
from typing import Any

from app.learning.evolution_models import EvolutionProposal


class EvolutionAdvisor:
    """
    Uses the local AI as a read-only evolution advisor.

    The advisor may analyze the project and propose improvements,
    but it never edits files or executes generated code.
    """

    def __init__(self, ai_provider):
        self.ai_provider = ai_provider

    async def propose(
        self,
        *,
        target: str,
        context: dict[str, Any],
    ) -> EvolutionProposal:
        prompt = self._build_prompt(target, context)

        response = await self.ai_provider.generate(
            message=prompt,
            conversation_id="evolution-advisor",
            context=context,
        )

        data = self._parse_response(response)

        return EvolutionProposal(
            proposal_id=str(data["proposal_id"]),
            title=str(data["title"]),
            description=str(data["description"]),
            category=str(data.get("category", "code_analysis")),
            target=str(data.get("target", target)),
            expected_gain=float(data.get("expected_gain", 0.0)),
            confidence=float(data.get("confidence", 0.0)),
            risk=float(data.get("risk", 1.0)),
            evidence=list(data.get("evidence", [])),
            metadata={
                "advisor": "local_ai",
                "raw_response": response,
            },
        )

    @staticmethod
    def _build_prompt(
        target: str,
        context: dict[str, Any],
    ) -> str:
        return f"""
You are the evolution advisor for a local software project.

Your job is to analyze the supplied project context and propose ONE
high-value, concrete improvement for the target: {target}.

IMPORTANT:
- Do not claim that you changed any files.
- Do not execute commands.
- Do not invent files that are not present.
- Prefer small, testable improvements.
- Use previous successful and failed evolution patterns.
- Reject vague suggestions such as "improve performance" without
  identifying what should change and why.
- The proposal must be testable.
- Return ONLY valid JSON.
- No Markdown.
- No code fences.

Required JSON shape:
{{
  "proposal_id": "advisor-unique-id",
  "title": "specific improvement title",
  "description": "specific explanation of the proposed improvement",
  "category": "code_analysis",
  "target": "{target}",
  "expected_gain": 0.0,
  "confidence": 0.0,
  "risk": 0.0,
  "evidence": [
    "specific evidence from the project context"
  ]
}}

PROJECT CONTEXT:
The provider supplies the project context separately.
Analyze that supplied context and do not request it again.
""".strip()

    @staticmethod
    def _parse_response(response: str) -> dict[str, Any]:
        text = response.strip()

        if not text:
            raise ValueError("Evolution advisor returned empty response")

        # First try the complete response.
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Some local models may accidentally add surrounding text.
            start = text.find("{")
            end = text.rfind("}")

            if start < 0 or end <= start:
                raise ValueError(
                    "Evolution advisor did not return valid JSON"
                )

            try:
                data = json.loads(text[start:end + 1])
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Evolution advisor returned malformed JSON"
                ) from exc

        if not isinstance(data, dict):
            raise ValueError("Evolution advisor response must be an object")

        required = {
            "proposal_id",
            "title",
            "description",
        }

        missing = required - data.keys()

        if missing:
            raise ValueError(
                f"Evolution advisor response missing fields: "
                f"{', '.join(sorted(missing))}"
            )

        return data
