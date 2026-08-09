from app.learning.evolution_report import EvolutionReportBuilder
from app.learning.execution_boundary import ExecutionAuthorization


def test_evolution_report_summarizes_full_lifecycle():
    proposal = type(
        "Proposal",
        (),
        {"proposal_id": "proposal-report-1"},
    )()

    evaluation = type(
        "Evaluation",
        (),
        {"accepted": True},
    )()

    evolution = type(
        "Evolution",
        (),
        {
            "proposal": proposal,
            "evaluation": evaluation,
        },
    )()

    learning = type(
        "Learning",
        (),
        {"accepted": True},
    )()

    review = type(
        "Review",
        (),
        {"status": "approved"},
    )()

    execution = ExecutionAuthorization(
        allowed=True,
        reason="execution_authorized",
    )

    dry_run = type(
        "DryRun",
        (),
        {
            "files": (
                "app/learning/code_intent.py",
            ),
        },
    )()

    result = type(
        "Result",
        (),
        {
            "learning": learning,
            "evolution": evolution,
            "review": review,
            "execution": execution,
            "dry_run": dry_run,
        },
    )()

    report = EvolutionReportBuilder().build(result)

    assert report.learning_accepted is True
    assert report.proposal_id == "proposal-report-1"
    assert report.evaluation_accepted is True
    assert report.review_status == "approved"
    assert report.execution_allowed is True
    assert report.execution_reason == "execution_authorized"
    assert report.dry_run_available is True
    assert report.dry_run_files == (
        "app/learning/code_intent.py",
    )


def test_evolution_report_handles_learning_only():
    learning = type(
        "Learning",
        (),
        {"accepted": True},
    )()

    result = type(
        "Result",
        (),
        {
            "learning": learning,
            "evolution": None,
            "review": None,
            "execution": None,
            "dry_run": None,
        },
    )()

    report = EvolutionReportBuilder().build(result)

    assert report.learning_accepted is True
    assert report.proposal_id is None
    assert report.evaluation_accepted is None
    assert report.review_status is None
    assert report.execution_allowed is None
    assert report.dry_run_available is False
    assert report.dry_run_files == ()
    assert report.execution_reason is None
