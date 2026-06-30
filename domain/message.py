from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from .aggregate import AggregateRoot
from .exceptions import ValidationError
from .identity import Identity
from .text import Text


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(eq=False, slots=True)
class Message(AggregateRoot[Identity]):
    """
    Message Entity.

    A Message represents a single immutable interaction inside a
    Conversation. Its identity never changes, while its content may evolve
    through explicit domain operations.
    """

    role: MessageRole
    content: Text
    created_at: datetime

    def __post_init__(self) -> None:
        super().__post_init__()

    @classmethod
    def create(
        cls,
        *,
        role: MessageRole,
        content: str | Text,
        message_id: Identity | None = None,
        created_at: datetime | None = None,
    ) -> Message:
        return cls(
            id=message_id or Identity.new(),
            role=role,
            content=content if isinstance(content, Text) else Text(content),
            created_at=created_at or datetime.now(UTC),
        )

    def update_content(
        self,
        content: str | Text,
    ) -> None:
        new_content = (
            content
            if isinstance(content, Text)
            else Text(content)
        )

        if new_content == self.content:
            raise ValidationError(
                "Message content must be different."
            )

        self.content = new_content