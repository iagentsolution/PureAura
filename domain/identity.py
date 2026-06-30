from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .value_objects import ValueObject


@dataclass(frozen=True, slots=True)
class Identity(ValueObject):
    """
    Immutable domain identifier.
    """

    value: UUID = field(default_factory=uuid4)

    @classmethod
    def new(cls) -> "Identity":
        return cls()

    @classmethod
    def from_string(cls, value: str) -> "Identity":
        return cls(UUID(value))

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Identity({self.value})"