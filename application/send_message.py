from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from application.contracts import (
    AuraAnalyzer,
    MessageGenerator,
    MissionGenerator,
    ProgressTracker,
)
from application.use_case import UseCase
from domain.result import Result


@dataclass(slots=True, frozen=True)
class SendMessageRequest:
    message: str


@dataclass(slots=True, frozen=True)
class SendMessageResponse:
    reply: str
    aura: dict[str, Any]
    missions: list[dict[str, Any]]
    progress: dict[str, Any]


class SendMessageUseCase(
    UseCase[
        SendMessageRequest,
        Result[SendMessageResponse, Exception],
    ]
):
    def __init__(
        self,
        message_generator: MessageGenerator,
        aura_analyzer: AuraAnalyzer,
        mission_generator: MissionGenerator,
        progress_tracker: ProgressTracker,
    ) -> None:
        self._message_generator = message_generator
        self._aura_analyzer = aura_analyzer
        self._mission_generator = mission_generator
        self._progress_tracker = progress_tracker

    async def execute(
        self,
        request: SendMessageRequest,
    ) -> Result[SendMessageResponse, Exception]:
        reply_result = await self._message_generator.send_message(
            request.message,
        )

        if reply_result.is_failure:
            return Result.fail(reply_result.error)

        aura_result = await self._aura_analyzer.analyze(
            reply_result.value,
        )

        if aura_result.is_failure:
            return Result.fail(aura_result.error)

        missions_result = await self._mission_generator.generate(
            message=reply_result.value,
            aura=aura_result.value,
        )

        if missions_result.is_failure:
            return Result.fail(missions_result.error)

        progress_result = self._progress_tracker.update(
            message=reply_result.value,
            aura=aura_result.value,
            missions=missions_result.value,
        )

        if progress_result.is_failure:
            return Result.fail(progress_result.error)

        return Result.ok(
            SendMessageResponse(
                reply=reply_result.value,
                aura=aura_result.value,
                missions=missions_result.value,
                progress=progress_result.value,
            )
        )