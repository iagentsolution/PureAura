from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Self, TypeVar

IdT = TypeVar("IdT")


@dataclass(eq=False, slots=True)
class Entity(Generic[IdT]):
    """
    Base class for all Domain Entities.
    """

    id: IdT = field(compare=False)

    @property
    def identity(self) -> IdT:
        return self.id

    def same_identity_as(self, other: Self) -> bool:
        return type(self) is type(other) and self.id == other.id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.same_identity_as(other)

    def __hash__(self) -> int:
        return hash((type(self), self.id))