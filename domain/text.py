from __future__ import annotations

from dataclasses import dataclass

from .exceptions import ValidationError
from .value_objects import ValueObject


@dataclass(frozen=True, slots=True)
class Text(ValueObject):
    """
    Immutable normalized text Value Object.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = " ".join(self.value.strip().split())

        if not normalized:
            raise ValidationError("Text cannot be empty.")

        object.__setattr__(self, "value", normalized)

    @property
    def is_empty(self) -> bool:
        return not self.value

    @property
    def length(self) -> int:
        return len(self.value)

    def contains(
        self,
        text: str,
        *,
        ignore_case: bool = False,
    ) -> bool:
        source = self.value.casefold() if ignore_case else self.value
        target = text.casefold() if ignore_case else text
        return target in source

    def startswith(
        self,
        prefix: str,
        *,
        ignore_case: bool = False,
    ) -> bool:
        source = self.value.casefold() if ignore_case else self.value
        target = prefix.casefold() if ignore_case else prefix
        return source.startswith(target)

    def endswith(
        self,
        suffix: str,
        *,
        ignore_case: bool = False,
    ) -> bool:
        source = self.value.casefold() if ignore_case else self.value
        target = suffix.casefold() if ignore_case else suffix
        return source.endswith(target)

    def lower(self) -> "Text":
        return Text(self.value.lower())

    def upper(self) -> "Text":
        return Text(self.value.upper())

    def casefold(self) -> "Text":
        return Text(self.value.casefold())

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)