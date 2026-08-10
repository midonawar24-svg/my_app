from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.learning.evolution_orchestrator import (
    EvolutionFlowResult,
    EvolutionOrchestrator,
)
from app.learning.evolution_context import EvolutionContextBuilder
from app.learning.models import LearningCandidate
from app.learning.pipeline import LearningPipeline
from app.learning.evolution_decision import EvolutionDecision, EvolutionDecisionLayer
from app.learning.execution_boundary import ExecutionAuthorization, ExecutionBoundary
from app.learning.execution_plan import ExecutionPlanBuilder
from app.learning.dry_run import DryRunReport, DryRunRunner
from app.learning.evolution_report import EvolutionReport
from app.learning.review_gate import HumanReviewGate, ReviewDecision


@dataclass(frozen=True)
class LearningEvolutionResult:
    learning: Any
    evolution: EvolutionFlowResult | None
    decision: EvolutionDecision | None = None
    review: ReviewDecision | None = None
    execution: ExecutionAuthorization | None = None
    dry_run: DryRunReport | None = None
    report: EvolutionReport | None = None


class LearningEvolutionFlow:
    """
    Connects the learning pipeline to the evolution pipeline.

    Learning is persisted first.
    Evolution proposals are generated only from accepted learning.
    No source code is edited or executed here.
    """

    def __init__(
        self,
        learning_pipeline: LearningPipeline,
        evolution_orchestrator: EvolutionOrchestrator | None = None,
        ai_provider=None,
        evolution_store=None,
        event_bus=None,
    ):
        self.learning_pipeline = learning_pipeline
        self.evolution_orchestrator = (
            evolution_orchestrator
            or EvolutionOrchestrator(
                ai_provider=ai_provider,
                evolution_store=evolution_store,
                event_bus=event_bus,
            )
        )
        self.evolution_context = EvolutionContextBuilder(
            project_root=Path("."),
            evolution_history=Path(".evolution_store.json"),
        )
        self.decision_layer = EvolutionDecisionLayer()
        self.review_gate = HumanReviewGate()
        self.execution_boundary = ExecutionBoundary()

    def review(
        self,
        result: LearningEvolutionResult,
        *,
        decision: str,
        reviewer: str = "human",
        note: str = "",
    ) -> LearningEvolutionResult:
        proposal_id = ""

        if result.evolution is not None:
            proposal_id = result.evolution.proposal.proposal_id

        review = self.review_gate.review(
            proposal_id=proposal_id,
            decision=decision,
            reviewer=reviewer,
            note=note,
        )

        return LearningEvolutionResult(
            learning=result.learning,
            evolution=result.evolution,
            decision=result.decision,
            review=review,
        )

    def authorize_execution(
        self,
        result: LearningEvolutionResult,
        *,
        validation_passed: bool,
    ) -> LearningEvolutionResult:
        proposal_id = ""

        if result.evolution is not None:
            proposal_id = result.evolution.proposal.proposal_id

        review_status = ""
        approved = False
        approved_proposal_id = None

        if result.review is not None:
            review_status = result.review.status
            approved = result.review.approved
            approved_proposal_id = result.review.metadata.get("proposal_id")

        execution = self.execution_boundary.authorize(
            proposal_id=proposal_id,
            review_status=review_status,
            approved=approved,
            validation_passed=validation_passed,
            approved_proposal_id=approved_proposal_id,
        )

        return LearningEvolutionResult(
            learning=result.learning,
            evolution=result.evolution,
            decision=result.decision,
            review=result.review,
            execution=execution,
        )

    def dry_run(
        self,
        result: LearningEvolutionResult,
        *,
        files: tuple[str, ...] = (),
    ) -> LearningEvolutionResult:
        if result.evolution is None or result.execution is None:
            return LearningEvolutionResult(
                learning=result.learning,
                evolution=result.evolution,
                decision=result.decision,
                review=result.review,
                execution=result.execution,
                dry_run=None,
            )

        proposal = result.evolution.proposal

        plan = ExecutionPlanBuilder().build_from_proposal(
            proposal,
            files=files,
        )

        report = DryRunRunner().preview(
            plan,
            result.execution,
        )

        return LearningEvolutionResult(
            learning=result.learning,
            evolution=result.evolution,
            decision=result.decision,
            review=result.review,
            execution=result.execution,
            dry_run=report,
        )

    def build_report(
        self,
        result: LearningEvolutionResult,
    ) -> LearningEvolutionResult:
        from app.learning.evolution_report import EvolutionReportBuilder

        report = EvolutionReportBuilder().build(result)

        return LearningEvolutionResult(
            learning=result.learning,
            evolution=result.evolution,
            decision=result.decision,
            review=result.review,
            execution=result.execution,
            dry_run=result.dry_run,
            report=report,
        )

    async def process(
        self,
        message: str,
        *,
        conversation_id: str | None = None,
        context: dict[str, Any] | None = None,
        source: str = "teacher",
        confidence: float = 0.0,
        category: str = "unknown",
        should_remember: bool = False,
        metadata: dict[str, Any] | None = None,
        reply: str | None = None,
        target: str = "local_ai",
        expected_gain: float = 0.0,
        risk: float = 0.0,
    ) -> LearningEvolutionResult:
        discovery_context = self.evolution_context.build()

        merged_context = dict(context or {})
        merged_context.update(discovery_context)

        learning_result = await self.learning_pipeline.learn(
            message,
            conversation_id=conversation_id,
            context=merged_context,
            source=source,
            confidence=confidence,
            category=category,
            should_remember=should_remember,
            metadata=metadata,
            reply=reply,
        )

        candidate = getattr(learning_result, "candidate", None)

        if candidate is None:
            candidate = getattr(learning_result, "learning_candidate", None)

        if candidate is None:
            return LearningEvolutionResult(
                learning=learning_result,
                evolution=None,
                decision=self.decision_layer.decide(
                    learning_accepted=False,
                    evaluation=None,
                ),
            )

        if not getattr(learning_result, "accepted", False):
            return LearningEvolutionResult(
                learning=learning_result,
                evolution=None,
                decision=self.decision_layer.decide(
                    learning_accepted=False,
                    evaluation=None,
                ),
            )

        evolution = self.evolution_orchestrator.process(
            candidate,
            target=target,
            expected_gain=expected_gain,
            risk=risk,
        )

        decision = self.decision_layer.decide(
            learning_accepted=learning_result.accepted,
            evaluation=evolution.evaluation,
        )

        return LearningEvolutionResult(
            learning=learning_result,
            evolution=evolution,
            decision=decision,
        )
