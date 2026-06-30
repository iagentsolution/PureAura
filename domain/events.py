from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True, kw_only=True)
class DomainEvent:
    """
    Base class for every Domain Event.
    """

    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    @property
    def event_name(self) -> str:
        return self.__class__.__name__

    @property
    def event_version(self) -> int:
        return 1

    def serialize(self) -> dict[str, str]:
        return {
            "event_id": str(self.event_id),
            "event_name": self.event_name,
            "event_version": str(self.event_version),
            "occurred_at": self.occurred_at.isoformat(),
        }