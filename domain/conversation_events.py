from __future__ import annotations

from dataclasses import dataclass

from .events import DomainEvent
from .identity import Identity
from .message import MessageRole


@dataclass(frozen=True, slots=True, kw_only=True)
class ConversationCreated(DomainEvent):
    """
    Raised when a Conversation aggregate is created.
    """

    conversation_id: Identity


@dataclass(frozen=True, slots=True, kw_only=True)
class MessageAdded(DomainEvent):
    """
    Raised after a Message has been added to a Conversation.
    """

    conversation_id: Identity
    message_id: Identity
    role: MessageRole


@dataclass(frozen=True, slots=True, kw_only=True)
class MessageRemoved(DomainEvent):
    """
    Raised after a Message has been removed from a Conversation.
    """

    conversation_id: Identity
    message_id: Identity


@dataclass(frozen=True, slots=True, kw_only=True)
class ConversationCleared(DomainEvent):
    """
    Raised when every Message has been removed from a Conversation.
    """

    conversation_id: Identity


@dataclass(frozen=True, slots=True, kw_only=True)
class ConversationArchived(DomainEvent):
    """
    Raised when a Conversation becomes read-only or archived.
    """

    conversation_id: Identity