from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .exceptions import DomainError

ContextT = TypeVar("ContextT")


class PolicyViolationError(DomainError):
    """
    Raised when a domain policy is violated.
    """

    __slots__ = ()


class Policy(ABC, Generic[ContextT]):
    """
    Base Domain Policy.

    Policies express business decisions that determine whether an operation
    is permitted within a given business context.

    Unlike Specifications, which describe business predicates, Policies
    represent authorization or permission decisions inside the domain model.
    """

    __slots__ = ()

    @abstractmethod
    def is_allowed(self, context: ContextT) -> bool:
        raise NotImplementedError

    def __call__(self, context: ContextT) -> bool:
        return self.is_allowed(context)

    def ensure(self, context: ContextT) -> None:
        if not self.is_allowed(context):
            raise PolicyViolationError(
                f"{self.__class__.__name__} policy was not satisfied."
            )