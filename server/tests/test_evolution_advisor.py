import asyncio
import pytest

from app.learning.evolution_advisor import EvolutionAdvisor


class StubAIProvider:
    def __init__(self, response: str):
        self.response = response
        self.calls = []

    async def generate(self, message, conversation_id="", context=None):
        self.calls.append({
            "message": message,
            "conversation_id": conversation_id,
            "context": context,
        })
        return self.response


def test_advisor_builds_proposal_from_local_ai_json():
    provider = StubAIProvider(
        '{"proposal_id":"advisor-1",'
        '"title":"Improve discovery context",'
        '"description":"Use discovered domain files in proposal evidence",'
        '"category":"code_analysis",'
        '"target":"local_ai",'
        '"expected_gain":0.8,'
        '"confidence":0.9,'
        '"risk":0.1,'
        '"evidence":["domain_count:16"]}'
    )

    context = {
        "has_project_analysis": True,
        "has_evolution_domains": True,
        "domain_count": 16,
    }

    proposal = asyncio.run(EvolutionAdvisor(provider).propose(
        target="local_ai",
        context=context,
    ))

    assert proposal.proposal_id == "advisor-1"
    assert proposal.title == "Improve discovery context"
    assert proposal.expected_gain == 0.8
    assert proposal.confidence == 0.9
    assert proposal.risk == 0.1
    assert proposal.metadata["advisor"] == "local_ai"

    assert len(provider.calls) == 1
    assert provider.calls[0]["conversation_id"] == "evolution-advisor"
    assert provider.calls[0]["context"] == context


def test_advisor_rejects_invalid_response():
    provider = StubAIProvider("not valid json")

    with pytest.raises(ValueError, match="valid JSON"):
        asyncio.run(EvolutionAdvisor(provider).propose(
            target="local_ai",
            context={"domain_count": 16},
        ))
