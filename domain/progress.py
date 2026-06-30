from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .aggregate import AggregateRoot
from .exceptions import BusinessRuleViolation
from .identity import Identity
from .score import Score


@dataclass(eq=False, slots=True)
class Progress(AggregateRoot[Identity]):
    """
    Progress Aggregate Root.

    Tracks the user's progress across missions. The aggregate guarantees
    consistency between completed and total missions while exposing
    meaningful domain operations instead of allowing arbitrary mutation.
    """

    completed_missions: int
    total_missions: int
    streak: int
    updated_at: datetime

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.total_missions < 0:
            raise BusinessRuleViolation(
                "Total missions cannot be negative."
            )

        if self.completed_missions < 0:
            raise BusinessRuleViolation(
                "Completed missions cannot be negative."
            )

        if self.completed_missions > self.total_missions:
            raise BusinessRuleViolation(
                "Completed missions cannot exceed total missions."
            )

        if self.streak < 0:
            raise BusinessRuleViolation(
                "Streak cannot be negative."
            )

    @classmethod
    def create(
        cls,
        *,
        progress_id: Identity | None = None,
        total_missions: int = 0,
    ) -> Progress:
        now = datetime.now(UTC)

        return cls(
            id=progress_id or Identity.new(),
            completed_missions=0,
            total_missions=max(0, total_missions),
            streak=0,
            updated_at=now,
        )

    @property
    def completion_rate(self) -> float:
        if self.total_missions == 0:
            return 0.0

        return self.completed_missions / self.total_missions

    @property
    def completion_score(self) -> Score:
        return Score(
            value=self.completion_rate * 100,
        )

    @property
    def remaining_missions(self) -> int:
        return self.total_missions - self.completed_missions

    @property
    def is_completed(self) -> bool:
        return (
            self.total_missions > 0
            and self.completed_missions == self.total_missions
        )

    def register_new_mission(self) -> None:
        self.total_missions += 1
        self._touch()

    def complete_mission(self) -> None:
        if self.completed_missions >= self.total_missions:
            raise BusinessRuleViolation(
                "There are no pending missions to complete."
            )

        self.completed_missions += 1
        self.streak += 1
        self._touch()

    def reset_streak(self) -> None:
        self.streak = 0
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)