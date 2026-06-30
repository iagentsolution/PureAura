from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from domain.message import MessageRole


@dataclass(slots=True)
class ChatMessageView:
    """
    Presentation-layer view of a chat message.

    This is a simple read-model used exclusively by the UI
    to render the conversation history. It is NOT the domain
    Message aggregate.
    """

    role: MessageRole
    content: str


@dataclass(slots=True)
class AuraView:
    mood: int = 0
    energy: int = 0
    chaos: int = 0
    purity: int = 0


@dataclass(slots=True)
class RankView:
    value: str = "Inicial"


@dataclass(slots=True)
class ProgressView:
    level: int = 1
    xp: int = 0
    rank: RankView = field(default_factory=RankView)


@dataclass(slots=True)
class ProfileView:
    name: str = "Usuario"
    aura: AuraView = field(default_factory=AuraView)
    progress: ProgressView = field(default_factory=ProgressView)


@dataclass(slots=True)
class BrainState:
    profile: ProfileView = field(default_factory=ProfileView)
    missions: list[Any] = field(default_factory=list)
    chat_history: list[ChatMessageView] = field(default_factory=list)