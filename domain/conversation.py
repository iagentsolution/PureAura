from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .aggregate import AggregateRoot
from .conversation_events import (
    ConversationArchived,
    ConversationCleared,
    ConversationCreated,
    MessageAdded,
    MessageRemoved,
)
from .exceptions import EntityNotFound
from .identity import Identity
from .message import Message


@dataclass(eq=False, slots=True)
class Conversation(AggregateRoot[Identity]):
    """
    Conversation Aggregate Root.

    The Conversation is responsible for maintaining the lifecycle of its
    Messages and enforcing aggregate invariants.
    """

    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def __post_init__(self) -> None:
        super().__post_init__()

    @classmethod
    def create(
        cls,
        *,
        conversation_id: Identity | None = None,
    ) -> Conversation:
        conversation = cls(
            id=conversation_id or Identity.new(),
        )

        conversation.record_event(
            ConversationCreated(
                conversation_id=conversation.id,
            )
        )

        return conversation

    def add_message(self, message: Message) -> None:
        self.messages.append(message)
        self._touch()

        self.record_event(
            MessageAdded(
                conversation_id=self.id,
                message_id=message.id,
                role=message.role,
            )
        )

    def remove_message(
        self,
        message_id: Identity,
    ) -> None:
        for index, message in enumerate(self.messages):
            if message.id == message_id:
                del self.messages[index]
                self._touch()

                self.record_event(
                    MessageRemoved(
                        conversation_id=self.id,
                        message_id=message_id,
                    )
                )

                if not self.messages:
                    self.record_event(
                        ConversationCleared(
                            conversation_id=self.id,
                        )
                    )

                return

        raise EntityNotFound(
            f"Message '{message_id}' was not found."
        )

    def clear(self) -> None:
        if not self.messages:
            return

        self.messages.clear()
        self._touch()

        self.record_event(
            ConversationCleared(
                conversation_id=self.id,
            )
        )

    def archive(self) -> None:
        self.record_event(
            ConversationArchived(
                conversation_id=self.id,
            )
        )

    def message_count(self) -> int:
        return len(self.messages)

    @property
    def is_empty(self) -> bool:
        return not self.messages

    @property
    def last_message(self) -> Message | None:
        if not self.messages:
            return None

        return self.messages[-1]

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)