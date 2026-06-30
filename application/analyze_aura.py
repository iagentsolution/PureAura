from __future__ import annotations

from dataclasses import dataclass

from application.contracts import AuraAnalyzer
from application.use_case import UseCase
from domain.result import Result


@dataclass(slots=True, frozen=True)
class AnalyzeAuraRequest:
    message: str


@dataclass(slots=True, frozen=True)
class AnalyzeAuraResponse:
    aura: dict


class AnalyzeAuraUseCase(
    UseCase[
        AnalyzeAuraRequest,
        Result[AnalyzeAuraResponse, Exception],
    ]
):
    def __init__(
        self,
        aura_analyzer: AuraAnalyzer,
    ) -> None:
        self._aura_analyzer = aura_analyzer

    async def execute(
        self,
        request: AnalyzeAuraRequest,
    ) -> Result[AnalyzeAuraResponse, Exception]:
        result = await self._aura_analyzer.analyze(
            request.message,
        )

        if result.is_failure:
            return Result.fail(result.error)

        return Result.ok(
            AnalyzeAuraResponse(
                aura=result.value,
            )
        )