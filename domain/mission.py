from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from .aggregate import AggregateRoot
from .exceptions import BusinessRuleViolation
from .identity import Identity
from .text import Text


class MissionStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(eq=False, slots=True)
class Mission(AggregateRoot[Identity]):
    """
    Mission Aggregate Root.

    A Mission models a unit of work that progresses through a controlled
    lifecycle. State transitions are enforced by the aggregate.
    """

    title: Text
    description: Text
    status: MissionStatus
    created_at: datetime
    completed_at: datetime | None

    def __post_init__(self) -> None:
        super().__post_init__()

    @classmethod
    def create(
        cls,
        *,
        title: str | Text,
        description: str | Text,
        mission_id: Identity | None = None,
        created_at: datetime | None = None,
    ) -> Mission:
        return cls(
            id=mission_id or Identity.new(),
            title=title if isinstance(title, Text) else Text(title),
            description=(
                description
                if isinstance(description, Text)
                else Text(description)
            ),
            status=MissionStatus.PENDING,
            created_at=created_at or datetime.now(UTC),
            completed_at=None,
        )

    def start(self) -> None:
        if self.status is MissionStatus.COMPLETED:
            raise BusinessRuleViolation(
                "A completed mission cannot be started."
            )

        if self.status is MissionStatus.CANCELLED:
            raise BusinessRuleViolation(
                "A cancelled mission cannot be started."
            )

        if self.status is MissionStatus.IN_PROGRESS:
            return

        self.status = MissionStatus.IN_PROGRESS

    def complete(self) -> None:
        if self.status is MissionStatus.CANCELLED:
            raise BusinessRuleViolation(
                "A cancelled mission cannot be completed."
            )

        if self.status is MissionStatus.COMPLETED:
            return

        self.status = MissionStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        if self.status is MissionStatus.COMPLETED:
            raise BusinessRuleViolation(
                "A completed mission cannot be cancelled."
            )

        if self.status is MissionStatus.CANCELLED:
            return

        self.status = MissionStatus.CANCELLED

    def update_title(
        self,
        title: str | Text,
    ) -> None:
        self.title = (
            title
            if isinstance(title, Text)
            else Text(title)
        )

    def update_description(
        self,
        description: str | Text,
    ) -> None:
        self.description = (
            description
            if isinstance(description, Text)
            else Text(description)
        )

    @property
    def is_pending(self) -> bool:
        return self.status is MissionStatus.PENDING

    @property
    def is_active(self) -> bool:
        return self.status is MissionStatus.IN_PROGRESS

    @property
    def is_completed(self) -> bool:
        return self.status is MissionStatus.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        return self.status is MissionStatus.CANCELLED