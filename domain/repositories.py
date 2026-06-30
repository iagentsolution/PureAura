from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .conversation import Conversation
from .mission import Mission
from .progress import Progress
from .user import User

AggregateT = TypeVar("AggregateT")
IdT = TypeVar("IdT")


class Repository(ABC, Generic[AggregateT, IdT]):
    """
    Base abstraction for Aggregate repositories.

    Repositories provide the collection-like interface through which
    Application interacts with Aggregate Roots.

    Implementations belong exclusively to Infrastructure.
    """

    __slots__ = ()

    @abstractmethod
    async def exists(self, entity_id: IdT) -> bool:
        """
        Returns whether an aggregate exists.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, entity_id: IdT) -> AggregateT | None:
        """
        Returns an aggregate or None.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(self, aggregate: AggregateT) -> None:
        """
        Marks a newly created aggregate for persistence.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, aggregate: AggregateT) -> None:
        """
        Persists modifications made to an existing aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, aggregate: AggregateT) -> None:
        """
        Removes an aggregate.
        """
        raise NotImplementedError


class ConversationRepository(
    Repository[Conversation, str],
    ABC,
):
    __slots__ = ()


class UserRepository(
    Repository[User, str],
    ABC,
):
    __slots__ = ()


class MissionRepository(
    Repository[Mission, str],
    ABC,
):
    __slots__ = ()


class ProgressRepository(
    Repository[Progress, str],
    ABC,
):
    __slots__ = ()