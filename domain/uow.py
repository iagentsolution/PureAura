from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType


class UnitOfWork(ABC):
    """
    Domain abstraction representing a transactional boundary.
    """

    __slots__ = ()

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def committed(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def rolled_back(self) -> bool:
        raise NotImplementedError