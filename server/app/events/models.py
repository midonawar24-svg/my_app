from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class EvolutionEvent:
    event_id: str
    event_type: str
    source: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    payload: dict[str, Any] = field(default_factory=dict)
