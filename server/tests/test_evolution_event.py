from app.events.models import EvolutionEvent


def test_evolution_event_contract():
    event = EvolutionEvent(
        event_id="event-1",
        event_type="evolution.created",
        source="evolution",
        payload={
            "proposal_id": "proposal-1",
        },
    )

    assert event.event_id == "event-1"
    assert event.event_type == "evolution.created"
    assert event.source == "evolution"
    assert event.payload["proposal_id"] == "proposal-1"
    assert event.created_at


def test_evolution_event_is_immutable():
    event = EvolutionEvent(
        event_id="event-1",
        event_type="evolution.created",
        source="evolution",
    )

    try:
        event.event_id = "changed"
    except AttributeError:
        pass
    else:
        raise AssertionError("EvolutionEvent must be immutable")
