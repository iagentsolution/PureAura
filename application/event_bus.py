from __future__ import annotations

from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import TypeVar

from domain.events import DomainEvent

EventT = TypeVar("EventT", bound=DomainEvent)
Handler = Callable[[EventT], Awaitable[None]]


class EventBus:
    """
    In-process application event bus.
    """

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Handler]] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[EventT],
        handler: Handler,
    ) -> None:
        self._handlers[event_type].append(handler)

    async def publish(
        self,
        event: DomainEvent,
    ) -> None:
        for handler in self._handlers.get(type(event), ()):
            await handler(event)

    async def publish_all(
        self,
        events: list[DomainEvent],
    ) -> None:
        for event in events:
            await self.publish(event)