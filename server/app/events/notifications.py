from dataclasses import dataclass, field
from typing import Any

from app.events.models import EvolutionEvent


@dataclass(frozen=True)
class EvolutionNotification:
    notification_id: str
    notification_type: str
    title: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)


class EvolutionNotificationSubscriber:
    """
    Converts evolution events into notifications.

    This subscriber does not modify project code and does not
    communicate directly with Chat or the AI provider.
    """

    def __init__(self):
        self.notifications: list[EvolutionNotification] = []

    def handle(self, event: EvolutionEvent) -> EvolutionNotification:
        if event.event_type == "evolution.evaluated":
            notification = EvolutionNotification(
                notification_id=f"{event.event_id}:notification",
                notification_type="evolution.evaluated",
                title="Evolution evaluated",
                message=(
                    f"Proposal {event.payload.get('proposal_id', '')} "
                    f"was evaluated with score "
                    f"{event.payload.get('score', 0.0)}."
                ),
                payload=dict(event.payload),
            )

        elif event.event_type == "evolution.duplicate_skipped":
            notification = EvolutionNotification(
                notification_id=f"{event.event_id}:notification",
                notification_type="evolution.duplicate_skipped",
                title="Duplicate evolution skipped",
                message=(
                    f"Proposal {event.payload.get('proposal_id', '')} "
                    "was skipped because the evolution was already seen."
                ),
                payload=dict(event.payload),
            )

        else:
            raise ValueError(
                f"Unsupported evolution event: {event.event_type}"
            )

        self.notifications.append(notification)
        return notification
