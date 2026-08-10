from app.events.factory import EvolutionEventFactory


def test_factory_builds_evaluated_event():
    event = EvolutionEventFactory().evaluated(
        event_id="factory-1",
        proposal_id="proposal-1",
        target="local_ai",
        accepted=True,
        score=0.93,
        reason="accepted",
    )

    assert event.event_id == "factory-1"
    assert event.event_type == "evolution.evaluated"
    assert event.source == "evolution_orchestrator"
    assert event.payload == {
        "proposal_id": "proposal-1",
        "target": "local_ai",
        "accepted": True,
        "score": 0.93,
        "reason": "accepted",
    }


def test_factory_builds_duplicate_event():
    event = EvolutionEventFactory().duplicate_skipped(
        event_id="factory-2",
        proposal_id="proposal-2",
        target="local_ai",
        fingerprint="fp-2",
        reason="evolution_already_seen",
    )

    assert event.event_id == "factory-2"
    assert event.event_type == "evolution.duplicate_skipped"
    assert event.payload["proposal_id"] == "proposal-2"
    assert event.payload["fingerprint"] == "fp-2"


def test_factory_returns_immutable_event():
    event = EvolutionEventFactory().evaluated(
        event_id="factory-3",
        proposal_id="proposal-3",
        target="local_ai",
        accepted=False,
        score=0.2,
        reason="score_too_low",
    )

    try:
        event.event_type = "changed"
    except AttributeError:
        pass
    else:
        raise AssertionError("Factory events must remain immutable")
