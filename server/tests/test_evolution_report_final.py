from app.learning.evolution_report import EvolutionReportBuilder


def test_final_evolution_report_contains_lifecycle_state():
    class Learning:
        accepted = True

    class Proposal:
        proposal_id = "proposal-final"

    class Evaluation:
        accepted = True

    class Evolution:
        proposal = Proposal()
        evaluation = Evaluation()

    class Review:
        status = "approved"

    class Execution:
        allowed = True
        reason = "execution_authorized"

    class DryRun:
        files = ("app/learning/example.py",)

    class Result:
        learning = Learning()
        evolution = Evolution()
        review = Review()
        execution = Execution()
        dry_run = DryRun()

    report = EvolutionReportBuilder().build(Result())

    assert report.learning_accepted is True
    assert report.proposal_id == "proposal-final"
    assert report.evaluation_accepted is True
    assert report.review_status == "approved"
    assert report.execution_allowed is True
    assert report.execution_reason == "execution_authorized"
    assert report.dry_run_available is True
    assert report.dry_run_files == ("app/learning/example.py",)
