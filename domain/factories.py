from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, ParamSpec, TypeVar

P = ParamSpec("P")
ProductT = TypeVar("ProductT")


class Factory(ABC, Generic[P, ProductT]):
    """
    Base class for Domain Factories.

    Factories encapsulate complex creation logic when constructing an
    Entity, Aggregate or Value Object requires business knowledge that
    should not live inside the object itself.

    Implementations must remain pure domain components and must never
    depend on infrastructure concerns.
    """

    __slots__ = ()

    @abstractmethod
    def create(
        self,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> ProductT:
        raise NotImplementedError