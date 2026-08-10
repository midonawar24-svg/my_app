from app.events.models import EvolutionEvent
from app.events.notifications import EvolutionNotificationSubscriber


def test_evaluated_event_creates_notification():
    subscriber = EvolutionNotificationSubscriber()

    event = EvolutionEvent(
        event_id="event-1",
        event_type="evolution.evaluated",
        source="evolution_orchestrator",
        payload={
            "proposal_id": "proposal-1",
            "target": "local_ai",
            "accepted": True,
            "score": 0.925,
            "reason": "accepted",
        },
    )

    notification = subscriber.handle(event)

    assert notification.notification_type == "evolution.evaluated"
    assert notification.title == "Evolution evaluated"
    assert "proposal-1" in notification.message
    assert "0.925" in notification.message
    assert notification.payload["accepted"] is True
    assert subscriber.notifications == [notification]


def test_duplicate_event_creates_notification():
    subscriber = EvolutionNotificationSubscriber()

    event = EvolutionEvent(
        event_id="event-2",
        event_type="evolution.duplicate_skipped",
        source="evolution_orchestrator",
        payload={
            "proposal_id": "proposal-2",
            "target": "local_ai",
            "fingerprint": "fp-123",
            "reason": "evolution_already_seen",
        },
    )

    notification = subscriber.handle(event)

    assert notification.notification_type == "evolution.duplicate_skipped"
    assert notification.title == "Duplicate evolution skipped"
    assert "proposal-2" in notification.message
    assert notification.payload["fingerprint"] == "fp-123"


def test_unsupported_event_is_rejected():
    subscriber = EvolutionNotificationSubscriber()

    event = EvolutionEvent(
        event_id="event-3",
        event_type="unknown.event",
        source="test",
    )

    try:
        subscriber.handle(event)
    except ValueError as exc:
        assert "Unsupported evolution event" in str(exc)
    else:
        raise AssertionError("Unsupported events must be rejected")
