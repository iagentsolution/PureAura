from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ValueT = TypeVar("ValueT")
NewValueT = TypeVar("NewValueT")
ErrorT = TypeVar("ErrorT", bound=Exception)


@dataclass(frozen=True, slots=True)
class Result(Generic[ValueT, ErrorT]):
    """
    Represents the outcome of an operation.

    A Result contains either a successful value or an error,
    but never both simultaneously.
    """

    _value: ValueT | None = None
    _error: ErrorT | None = None

    def __post_init__(self) -> None:
        has_value = self._value is not None
        has_error = self._error is not None

        if has_value == has_error:
            raise ValueError(
                "Result must contain either a value or an error."
            )

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    @property
    def value(self) -> ValueT:
        if self.is_failure:
            raise self.error

        return self._value  # type: ignore[return-value]

    @property
    def error(self) -> ErrorT:
        if self.is_success:
            raise RuntimeError(
                "Successful Result does not contain an error."
            )

        return self._error  # type: ignore[return-value]

    def unwrap(self) -> ValueT:
        return self.value

    def unwrap_or(
        self,
        default: ValueT,
    ) -> ValueT:
        return self.value if self.is_success else default

    def map(
        self,
        mapper: Callable[[ValueT], NewValueT],
    ) -> Result[NewValueT, ErrorT]:
        if self.is_failure:
            return Result.fail(self.error)

        return Result.ok(
            mapper(self.value),
        )

    def bind(
        self,
        mapper: Callable[[ValueT], Result[NewValueT, ErrorT]],
    ) -> Result[NewValueT, ErrorT]:
        if self.is_failure:
            return Result.fail(self.error)

        return mapper(self.value)

    def on_success(
        self,
        action: Callable[[ValueT], None],
    ) -> Result[ValueT, ErrorT]:
        if self.is_success:
            action(self.value)

        return self

    def on_failure(
        self,
        action: Callable[[ErrorT], None],
    ) -> Result[ValueT, ErrorT]:
        if self.is_failure:
            action(self.error)

        return self

    @classmethod
    def ok(
        cls,
        value: ValueT,
    ) -> Result[ValueT, ErrorT]:
        return cls(_value=value)

    @classmethod
    def fail(
        cls,
        error: ErrorT,
    ) -> Result[ValueT, ErrorT]:
        return cls(_error=error)