from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping

from application.dto import (
    AnalyzeAuraResponse,
    ChatMessage,
    CompleteMissionResponse,
    GenerateMissionsResponse,
)


class AIProvider(ABC):
    @abstractmethod
    async def send_message(
        self,
        message: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def generate_message(
        self,
        message: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def json(
        self,
        messages: list[ChatMessage],
    ) -> Mapping[str, object]:
        raise NotImplementedError

    @abstractmethod
    async def analyze_aura(
        self,
        *,
        message: str,
    ) -> AnalyzeAuraResponse:
        raise NotImplementedError

    @abstractmethod
    async def generate_missions(
        self,
        *,
        message: str,
        aura: AnalyzeAuraResponse,
    ) -> GenerateMissionsResponse:
        raise NotImplementedError

    @abstractmethod
    async def complete_mission(
        self,
        *,
        mission_id: str,
    ) -> CompleteMissionResponse:
        raise NotImplementedError