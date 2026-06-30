from __future__ import annotations

from abc import ABC
from dataclasses import Field, fields
from typing import Any


class ValueObject(ABC):
    """
    Base class for all Value Objects.

    A Value Object is immutable and defined exclusively by the values of
    its attributes. It has no conceptual identity.
    """

    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if type(self) is not type(other):
            return False

        return all(
            getattr(self, field.name) == getattr(other, field.name)
            for field in self._fields()
        )

    def __hash__(self) -> int:
        return hash(
            tuple(
                getattr(self, field.name)
                for field in self._fields()
            )
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            field.name: getattr(self, field.name)
            for field in self._fields()
        }

    @classmethod
    def _fields(cls) -> tuple[Field[Any], ...]:
        return tuple(fields(cls))