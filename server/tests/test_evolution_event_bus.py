from app.events.bus import EvolutionEventBus
from app.events.models import EvolutionEvent


def test_event_bus_publishes_to_matching_subscribers():
    bus = EvolutionEventBus()
    received = []

    def handler(event):
        received.append(event)

    bus.subscribe("evolution.created", handler)

    event = EvolutionEvent(
        event_id="event-1",
        event_type="evolution.created",
        source="evolution",
    )

    result = bus.publish(event)

    assert result == [None]
    assert received == [event]


def test_event_bus_does_not_dispatch_to_other_event_types():
    bus = EvolutionEventBus()
    received = []

    bus.subscribe(
        "evolution.accepted",
        lambda event: received.append(event),
    )

    event = EvolutionEvent(
        event_id="event-1",
        event_type="evolution.created",
        source="evolution",
    )

    assert bus.publish(event) == []
    assert received == []


def test_event_bus_rejects_empty_event_type():
    bus = EvolutionEventBus()

    try:
        bus.subscribe("", lambda event: None)
    except ValueError as exc:
        assert str(exc) == "event_type cannot be empty"
    else:
        raise AssertionError("Expected ValueError")
