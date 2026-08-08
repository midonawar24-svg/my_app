from dataclasses import dataclass

from app.learning.models import LearningCandidate


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    reason: str


class LearningValidator:
    """
    Decides whether a learning candidate is eligible
    to continue toward memory.

    This validator does not write to memory.
    """

    def validate(
        self,
        candidate: LearningCandidate,
    ) -> ValidationResult:

        if not candidate.content.strip():
            return ValidationResult(
                accepted=False,
                reason="empty_content",
            )

        if not 0.0 <= candidate.confidence <= 1.0:
            return ValidationResult(
                accepted=False,
                reason="invalid_confidence",
            )

        if not candidate.should_remember:
            return ValidationResult(
                accepted=False,
                reason="memory_not_requested",
            )

        if candidate.confidence < 0.70:
            return ValidationResult(
                accepted=False,
                reason="confidence_too_low",
            )

        return ValidationResult(
            accepted=True,
            reason="accepted",
        )
