from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .aggregate import AggregateRoot
from .identity import Identity
from .score import Score
from .text import Text


@dataclass(eq=False, slots=True)
class Aura(AggregateRoot[Identity]):
    """
    Aura Aggregate Root.

    Represents the current domain interpretation of a user's emotional
    state. It is intentionally independent from any AI provider or
    inference engine.

    The aggregate only stores business information. How an Aura is
    produced belongs to a Domain Service.
    """

    summary: Text
    score: Score
    updated_at: datetime

    def __post_init__(self) -> None:
        super().__post_init__()

    @classmethod
    def create(
        cls,
        *,
        summary: str | Text,
        score: Score,
        aura_id: Identity | None = None,
        updated_at: datetime | None = None,
    ) -> Aura:
        return cls(
            id=aura_id or Identity.new(),
            summary=(
                summary
                if isinstance(summary, Text)
                else Text(summary)
            ),
            score=score,
            updated_at=updated_at or datetime.now(UTC),
        )

    def update_summary(
        self,
        summary: str | Text,
    ) -> None:
        self.summary = (
            summary
            if isinstance(summary, Text)
            else Text(summary)
        )
        self._touch()

    def update_score(
        self,
        score: Score,
    ) -> None:
        self.score = score
        self._touch()

    def update(
        self,
        *,
        summary: str | Text,
        score: Score,
    ) -> None:
        self.summary = (
            summary
            if isinstance(summary, Text)
            else Text(summary)
        )
        self.score = score
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)