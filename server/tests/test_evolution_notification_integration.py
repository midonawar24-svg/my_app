from app.events.bus import EvolutionEventBus
from app.events.models import EvolutionEvent
from app.events.notifications import EvolutionNotificationSubscriber


def test_event_bus_delivers_evolution_event_to_notification_subscriber():
    bus = EvolutionEventBus()
    subscriber = EvolutionNotificationSubscriber()

    bus.subscribe(
        "evolution.evaluated",
        subscriber.handle,
    )

    event = EvolutionEvent(
        event_id="event-integration-1",
        event_type="evolution.evaluated",
        source="evolution_orchestrator",
        payload={
            "proposal_id": "proposal-integration-1",
            "target": "local_ai",
            "accepted": True,
            "score": 0.93,
            "reason": "accepted",
        },
    )

    results = bus.publish(event)

    assert len(results) == 1
    assert results[0].notification_type == "evolution.evaluated"
    assert results[0].payload["proposal_id"] == "proposal-integration-1"

    assert len(subscriber.notifications) == 1
    assert subscriber.notifications[0] == results[0]


def test_duplicate_event_reaches_notification_subscriber():
    bus = EvolutionEventBus()
    subscriber = EvolutionNotificationSubscriber()

    bus.subscribe(
        "evolution.duplicate_skipped",
        subscriber.handle,
    )

    event = EvolutionEvent(
        event_id="event-integration-2",
        event_type="evolution.duplicate_skipped",
        source="evolution_orchestrator",
        payload={
            "proposal_id": "proposal-integration-2",
            "target": "local_ai",
            "fingerprint": "fingerprint-2",
            "reason": "evolution_already_seen",
        },
    )

    results = bus.publish(event)

    assert len(results) == 1
    assert results[0].notification_type == "evolution.duplicate_skipped"
    assert "proposal-integration-2" in results[0].message
    assert results[0].payload["fingerprint"] == "fingerprint-2"


def test_notification_layer_stays_independent_from_chat():
    subscriber = EvolutionNotificationSubscriber()

    event = EvolutionEvent(
        event_id="event-integration-3",
        event_type="evolution.evaluated",
        source="evolution_orchestrator",
        payload={
            "proposal_id": "proposal-integration-3",
            "accepted": False,
            "score": 0.4,
        },
    )

    notification = subscriber.handle(event)

    assert notification.notification_type == "evolution.evaluated"
    assert notification.payload["accepted"] is False
    assert not hasattr(notification, "chat_message")
    assert not hasattr(notification, "ai_provider")
