from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .aggregate import AggregateRoot
from .identity import Identity


@dataclass(eq=False, slots=True)
class User(AggregateRoot[Identity]):
    name: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        super().__post_init__()

    @classmethod
    def create(
        cls,
        *,
        name: str,
        user_id: Identity | None = None,
    ) -> "User":
        normalized_name = name.strip()

        return cls(
            id=user_id or Identity.new(),
            name=normalized_name,
        )

    def rename(self, name: str) -> None:
        normalized_name = name.strip()

        if normalized_name == self.name:
            return

        self.name = normalized_name
        self.updated_at = datetime.now(UTC)