from __future__ import annotations

from dataclasses import dataclass

from application.contracts import MissionGenerator, ProgressTracker
from application.use_case import UseCase
from domain.result import Result


@dataclass(slots=True, frozen=True)
class CompleteMissionRequest:
    mission_id: str


@dataclass(slots=True, frozen=True)
class CompleteMissionResponse:
    mission: dict
    progress: dict


class CompleteMissionUseCase(
    UseCase[
        CompleteMissionRequest,
        Result[CompleteMissionResponse, Exception],
    ]
):
    def __init__(
        self,
        mission_generator: MissionGenerator,
        progress_tracker: ProgressTracker,
    ) -> None:
        self._mission_generator = mission_generator
        self._progress_tracker = progress_tracker

    async def execute(
        self,
        request: CompleteMissionRequest,
    ) -> Result[CompleteMissionResponse, Exception]:
        mission_result = await self._mission_generator.complete(
            request.mission_id,
        )

        if mission_result.is_failure:
            return Result.fail(mission_result.error)

        progress_result = self._progress_tracker.reward(
            mission_result.value,
        )

        if progress_result.is_failure:
            return Result.fail(progress_result.error)

        return Result.ok(
            CompleteMissionResponse(
                mission=mission_result.value,
                progress=progress_result.value,
            )
        )