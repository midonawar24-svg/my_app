from app.learning.evolution_cycle_runner import EvolutionCycleRunner


def test_cycle_runner_contract():
    runner = EvolutionCycleRunner()

    result = runner.run(
        target="local_ai",
        context={"domain_count": 16},
    )

    assert result.cycle_id.startswith("run-")
    assert result.target == "local_ai"
    assert result.started_at
    assert result.finished_at is None
    assert result.result == "started"
    assert result.metadata["context"]["domain_count"] == 16
    assert result.metadata["execution"] == "not_started"


def test_cycle_runner_does_not_execute_project_changes():
    runner = EvolutionCycleRunner()

    result = runner.run(
        target="local_ai",
        context={},
    )

    assert result.metadata["execution"] == "not_started"
