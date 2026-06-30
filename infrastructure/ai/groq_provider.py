from __future__ import annotations

from collections.abc import Mapping

from application.contracts.ai import AIProvider
from application.dto import (
    AnalyzeAuraResponse,
    ChatMessage,
    CompleteMissionResponse,
    GenerateMissionsResponse,
)
from domain.message import MessageRole


class GroqProvider(AIProvider):
    def __init__(
        self,
        client: GroqClient,
        *,
        model: str,
    ) -> None:
        self._client = client
        self._model = model

    @classmethod
    def from_api_key(
        cls,
        *,
        api_key: str,
        model: str,
    ) -> "GroqProvider":
        return cls(
            client=GroqClient(api_key=api_key),
            model=model,
        )

    async def send_message(
        self,
        message: str,
    ) -> str:
        return await self.generate_message(message)

    async def generate_message(
        self,
        message: str,
    ) -> str:
        return await self.chat(
            [
                ChatMessage(
                    role=MessageRole.USER,
                    content=message,
                )
            ]
        )

    async def chat(
        self,
        messages: list[ChatMessage],
    ) -> str:
        return await self._client.chat(
            model=self._model,
            messages=messages,
        )

    async def json(
        self,
        messages: list[ChatMessage],
    ) -> Mapping[str, object]:
        return await self._client.json(
            model=self._model,
            messages=messages,
        )

    async def analyze_aura(
        self,
        *,
        message: str,
    ) -> AnalyzeAuraResponse:
        return await self._client.analyze_aura(
            model=self._model,
            message=message,
        )

    async def generate_missions(
        self,
        *,
        message: str,
        aura: AnalyzeAuraResponse,
    ) -> GenerateMissionsResponse:
        return await self._client.generate_missions(
            model=self._model,
            message=message,
            aura=aura,
        )

    async def complete_mission(
        self,
        *,
        mission_id: str,
    ) -> CompleteMissionResponse:
        return await self._client.complete_mission(
            mission_id=mission_id,
        )


class GroqClient:
    """
    Concrete Groq API client.

    Encapsulates all HTTP interaction with the Groq cloud API.
    This class is infrastructure-only and is never referenced
    outside the Composition Root or its own module.
    """

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def chat(
        self,
        *,
        model: str,
        messages: list[ChatMessage],
    ) -> str:
        raise NotImplementedError(
            "GroqClient.chat() requires a live Groq API connection."
        )

    async def json(
        self,
        *,
        model: str,
        messages: list[ChatMessage],
    ) -> Mapping[str, object]:
        raise NotImplementedError(
            "GroqClient.json() requires a live Groq API connection."
        )

    async def analyze_aura(
        self,
        *,
        model: str,
        message: str,
    ) -> AnalyzeAuraResponse:
        raise NotImplementedError(
            "GroqClient.analyze_aura() requires a live Groq API connection."
        )

    async def generate_missions(
        self,
        *,
        model: str,
        message: str,
        aura: AnalyzeAuraResponse,
    ) -> GenerateMissionsResponse:
        raise NotImplementedError(
            "GroqClient.generate_missions() requires a live Groq API connection."
        )

    async def complete_mission(
        self,
        *,
        mission_id: str,
    ) -> CompleteMissionResponse:
        raise NotImplementedError(
            "GroqClient.complete_mission() requires a live Groq API connection."
        )