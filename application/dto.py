from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.message import MessageRole

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """
    Lightweight DTO for AI provider communication.

    This is NOT the domain Message aggregate. It is a simple
    data-transfer object used exclusively at the Application /
    Infrastructure boundary to interact with AI providers.
    """

    role: MessageRole
    content: str


@dataclass(slots=True, frozen=True)
class AnalyzeAuraResponse:
    aura: dict[str, Any]


@dataclass(slots=True, frozen=True)
class GenerateMissionsResponse:
    missions: list[dict[str, Any]]


@dataclass(slots=True, frozen=True)
class CompleteMissionResponse:
    mission: dict[str, Any]