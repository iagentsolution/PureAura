from __future__ import annotations

from dataclasses import dataclass

from application.contracts import MissionGenerator
from application.use_case import UseCase
from domain.result import Result


@dataclass(slots=True, frozen=True)
class GenerateMissionsRequest:
    message: str
    aura: dict


@dataclass(slots=True, frozen=True)
class GenerateMissionsResponse:
    missions: list[dict]


class GenerateMissionsUseCase(
    UseCase[
        GenerateMissionsRequest,
        Result[GenerateMissionsResponse, Exception],
    ]
):
    def __init__(
        self,
        mission_generator: MissionGenerator,
    ) -> None:
        self._mission_generator = mission_generator

    async def execute(
        self,
        request: GenerateMissionsRequest,
    ) -> Result[GenerateMissionsResponse, Exception]:
        result = await self._mission_generator.generate(
            message=request.message,
            aura=request.aura,
        )

        if result.is_failure:
            return Result.fail(result.error)

        return Result.ok(
            GenerateMissionsResponse(
                missions=result.value,
            )
        )