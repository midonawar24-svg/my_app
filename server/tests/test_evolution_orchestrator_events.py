from app.events.bus import EvolutionEventBus
from app.learning.evolution_orchestrator import EvolutionOrchestrator
from app.learning.models import LearningCandidate
from app.learning.evolution_store import EvolutionStore


def make_candidate():
    return LearningCandidate(
        content="Improve evolution event handling",
        source="teacher",
        confidence=1.0,
        category="knowledge",
        should_remember=False,
    )


def test_orchestrator_publishes_evaluated_event(tmp_path):
    received = []

    bus = EvolutionEventBus()
    bus.subscribe(
        "evolution.evaluated",
        lambda event: received.append(event),
    )

    store = EvolutionStore(tmp_path / "evolution.json")

    orchestrator = EvolutionOrchestrator(
        evolution_store=store,
        event_bus=bus,
    )

    result = orchestrator.process(
        make_candidate(),
        target="local_ai",
        expected_gain=0.90,
        risk=0.05,
    )

    assert len(received) == 1

    event = received[0]

    assert event.event_type == "evolution.evaluated"
    assert event.source == "evolution_orchestrator"
    assert event.payload["proposal_id"] == result.proposal.proposal_id
    assert event.payload["target"] == "local_ai"
    assert event.payload["accepted"] is True
    assert event.payload["score"] == result.evaluation.score


def test_orchestrator_publishes_duplicate_event(tmp_path):
    received = []

    bus = EvolutionEventBus()
    bus.subscribe(
        "evolution.duplicate_skipped",
        lambda event: received.append(event),
    )

    store = EvolutionStore(tmp_path / "evolution.json")

    orchestrator = EvolutionOrchestrator(
        evolution_store=store,
        event_bus=bus,
    )

    candidate = make_candidate()

    first = orchestrator.process(
        candidate,
        target="local_ai",
        expected_gain=0.90,
        risk=0.05,
    )

    second = orchestrator.process(
        candidate,
        target="local_ai",
        expected_gain=0.90,
        risk=0.05,
    )

    assert first.proposal.metadata["fingerprint"]
    assert second.evaluation.reason == "evolution_already_seen"

    assert len(received) == 1

    event = received[0]

    assert event.event_type == "evolution.duplicate_skipped"
    assert event.source == "evolution_orchestrator"
    assert event.payload["proposal_id"] == second.proposal.proposal_id
    assert event.payload["target"] == "local_ai"
    assert event.payload["fingerprint"] == (
        second.proposal.metadata["fingerprint"]
    )
