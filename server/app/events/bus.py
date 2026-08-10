from collections import defaultdict
from collections.abc import Callable
from typing import Any

from app.events.models import EvolutionEvent


EventHandler = Callable[[EvolutionEvent], Any]


class EvolutionEventBus:
    """
    In-process event bus for evolution events.

    Publishing an event only dispatches it to registered subscribers.
    It does not modify project code and does not know about Chat or AI.
    """

    def __init__(self):
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event_type: str,
        handler: EventHandler,
    ) -> None:
        event_type = event_type.strip()

        if not event_type:
            raise ValueError("event_type cannot be empty")

        self._subscribers[event_type].append(handler)

    def publish(
        self,
        event: EvolutionEvent,
    ) -> list[Any]:
        handlers = self._subscribers.get(event.event_type, [])

        return [
            handler(event)
            for handler in handlers
        ]
