from hashlib import sha256
from typing import Any

from app.learning.evolution_memory import EvolutionMemory
from app.learning.evolution_models import EvolutionProposal
from app.learning.models import LearningCandidate


class EvolutionBridge:
    """
    Converts validated learning observations into evolution proposals.

    Evolution history is used as context for future proposals.
    This bridge only creates proposals.
    It never executes or modifies production code.
    """

    def __init__(self, evolution_memory: EvolutionMemory | None = None):
        self.evolution_memory = evolution_memory

    def build_proposal(
        self,
        candidate: LearningCandidate,
        *,
        target: str = "local_ai",
        expected_gain: float = 0.0,
        risk: float = 0.0,
        discovery_context: dict[str, Any] | None = None,
    ) -> EvolutionProposal:
        content = candidate.content.strip()

        if not content:
            raise ValueError(
                "Cannot create evolution proposal from empty learning"
            )

        if not 0.0 <= expected_gain <= 1.0:
            raise ValueError("expected_gain must be between 0 and 1")

        if not 0.0 <= risk <= 1.0:
            raise ValueError("risk must be between 0 and 1")

        digest = sha256(content.encode("utf-8")).hexdigest()[:16]
        fingerprint = sha256(
            f"{target}|{candidate.category}|{content}".encode("utf-8")
        ).hexdigest()

        proposal_id = f"learn-{digest}"

        metadata: dict[str, Any] = {
            "conversation_id": candidate.conversation_id,
            "learning_source": candidate.source,
            "fingerprint": fingerprint,
        }

        if self.evolution_memory is not None:
            metadata["evolution_memory"] = (
                self.evolution_memory.build_context(limit=10)
            )

        if discovery_context is not None:
            metadata["discovery_context"] = discovery_context

        title = f"Improve {target} from learned observation"

        description = (
            "Evolution candidate generated from a learning observation: "
            + content
        )

        return EvolutionProposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            category=candidate.category,
            target=target,
            expected_gain=expected_gain,
            confidence=candidate.confidence,
            risk=risk,
            evidence=[
                f"learning_source:{candidate.source}",
                f"learning_category:{candidate.category}",
            ],
            metadata=metadata,
        )
