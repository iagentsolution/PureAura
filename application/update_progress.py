from __future__ import annotations

from dataclasses import dataclass

from application.contracts import ProgressTracker
from application.use_case import UseCase
from domain.result import Result


@dataclass(slots=True, frozen=True)
class UpdateProgressRequest:
    message: str
    aura: dict
    missions: list[dict]


@dataclass(slots=True, frozen=True)
class UpdateProgressResponse:
    progress: dict


class UpdateProgressUseCase(
    UseCase[
        UpdateProgressRequest,
        Result[UpdateProgressResponse, Exception],
    ]
):
    def __init__(
        self,
        progress_tracker: ProgressTracker,
    ) -> None:
        self._progress_tracker = progress_tracker

    async def execute(
        self,
        request: UpdateProgressRequest,
    ) -> Result[UpdateProgressResponse, Exception]:
        result = self._progress_tracker.update(
            message=request.message,
            aura=request.aura,
            missions=request.missions,
        )

        if result.is_failure:
            return Result.fail(result.error)

        return Result.ok(
            UpdateProgressResponse(
                progress=result.value,
            )
        )