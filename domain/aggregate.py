from __future__ import annotations

from typing import Generic, TypeVar

from .entities import Entity
from .events import DomainEvent

IdT = TypeVar("IdT")


class AggregateRoot(Entity[IdT], Generic[IdT]):
    """
    Base class for Aggregate Roots.
    """

    __slots__ = ("_domain_events",)

    def __post_init__(self) -> None:
        super_post_init = getattr(super(), "__post_init__", None)
        if callable(super_post_init):
            super_post_init()

        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        return tuple(self._domain_events)

    @property
    def has_pending_events(self) -> bool:
        return bool(self._domain_events)

    def record_event(self, event: DomainEvent) -> DomainEvent:
        self._domain_events.append(event)
        return event

    def pull_events(self) -> tuple[DomainEvent, ...]:
        events = tuple(self._domain_events)
        self._domain_events.clear()
        return events

    def clear_events(self) -> None:
        self._domain_events.clear()