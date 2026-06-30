from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

CandidateT = TypeVar("CandidateT")


class Specification(ABC, Generic[CandidateT]):
    """
    Base Specification.

    Specifications encapsulate reusable business predicates that can be
    composed to express complex business rules while remaining independent
    from entities, repositories and infrastructure.
    """

    __slots__ = ()

    @abstractmethod
    def is_satisfied_by(self, candidate: CandidateT) -> bool:
        raise NotImplementedError

    def __call__(self, candidate: CandidateT) -> bool:
        return self.is_satisfied_by(candidate)

    def __and__(
        self,
        other: Specification[CandidateT],
    ) -> Specification[CandidateT]:
        return AndSpecification(self, other)

    def __or__(
        self,
        other: Specification[CandidateT],
    ) -> Specification[CandidateT]:
        return OrSpecification(self, other)

    def __invert__(self) -> Specification[CandidateT]:
        return NotSpecification(self)


class CompositeSpecification(Specification[CandidateT], ABC):
    """
    Base class for specifications composed from other specifications.
    """

    __slots__ = ()


class BinarySpecification(CompositeSpecification[CandidateT], ABC):
    """
    Base class for binary specifications.
    """

    __slots__ = ("_left", "_right")

    def __init__(
        self,
        left: Specification[CandidateT],
        right: Specification[CandidateT],
    ) -> None:
        self._left = left
        self._right = right


class AndSpecification(BinarySpecification[CandidateT]):
    """
    Logical AND.
    """

    __slots__ = ()

    def is_satisfied_by(self, candidate: CandidateT) -> bool:
        return (
            self._left.is_satisfied_by(candidate)
            and self._right.is_satisfied_by(candidate)
        )


class OrSpecification(BinarySpecification[CandidateT]):
    """
    Logical OR.
    """

    __slots__ = ()

    def is_satisfied_by(self, candidate: CandidateT) -> bool:
        return (
            self._left.is_satisfied_by(candidate)
            or self._right.is_satisfied_by(candidate)
        )


class NotSpecification(CompositeSpecification[CandidateT]):
    """
    Logical NOT.
    """

    __slots__ = ("_specification",)

    def __init__(
        self,
        specification: Specification[CandidateT],
    ) -> None:
        self._specification = specification

    def is_satisfied_by(self, candidate: CandidateT) -> bool:
        return not self._specification.is_satisfied_by(candidate)