from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from .events import DomainEvent


class DomainEventBus(ABC):
    """
    Domain abstraction for publishing Domain Events.

    The bus represents the outbound port through which the Domain notifies
    the outside world that something relevant has occurred.

    Concrete implementations may dispatch events synchronously,
    asynchronously, in-process, through message brokers or any other
    transport, but those concerns belong exclusively to Infrastructure.
    """

    __slots__ = ()

    @abstractmethod
    async def publish(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Publish a single Domain Event.
        """
        raise NotImplementedError

    async def publish_all(
        self,
        events: Sequence[DomainEvent],
    ) -> None:
        """
        Publish multiple Domain Events preserving their order.
        """
        for event in events:
            await self.publish(event)