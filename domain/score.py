from __future__ import annotations

from dataclasses import dataclass

from .exceptions import ValidationError
from .value_objects import ValueObject


@dataclass(frozen=True, slots=True)
class Score(ValueObject):
    value: float
    minimum: float = 0.0
    maximum: float = 100.0

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            raise ValidationError(
                "Minimum score cannot be greater than maximum score."
            )

        if not self.minimum <= self.value <= self.maximum:
            raise ValidationError(
                f"Score must be between {self.minimum} and {self.maximum}."
            )

    @property
    def percentage(self) -> float:
        span = self.maximum - self.minimum
        if span <= 0:
            return 1.0
        return (self.value - self.minimum) / span

    @property
    def remaining(self) -> float:
        return self.maximum - self.value

    @property
    def is_empty(self) -> bool:
        return self.value <= self.minimum

    @property
    def is_full(self) -> bool:
        return self.value >= self.maximum

    def increase(self, amount: float) -> "Score":
        return self.with_value(min(self.value + amount, self.maximum))

    def decrease(self, amount: float) -> "Score":
        return self.with_value(max(self.value - amount, self.minimum))

    def with_value(self, value: float) -> "Score":
        return Score(
            value=value,
            minimum=self.minimum,
            maximum=self.maximum,
        )

    def clamp(self) -> "Score":
        return self.with_value(
            min(max(self.value, self.minimum), self.maximum)
        )

    def __float__(self) -> float:
        return self.value