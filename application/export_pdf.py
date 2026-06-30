from __future__ import annotations

from dataclasses import dataclass

from application.contracts import PdfExporter
from application.use_case import UseCase
from domain.result import Result


@dataclass(slots=True, frozen=True)
class ExportPdfRequest:
    profile: dict
    aura: dict
    missions: list[dict]
    progress: dict


@dataclass(slots=True, frozen=True)
class ExportPdfResponse:
    file: bytes


class ExportPdfUseCase(
    UseCase[
        ExportPdfRequest,
        Result[ExportPdfResponse, Exception],
    ]
):
    def __init__(
        self,
        pdf_exporter: PdfExporter,
    ) -> None:
        self._pdf_exporter = pdf_exporter

    async def execute(
        self,
        request: ExportPdfRequest,
    ) -> Result[ExportPdfResponse, Exception]:
        result = await self._pdf_exporter.export(
            profile=request.profile,
            aura=request.aura,
            missions=request.missions,
            progress=request.progress,
        )

        if result.is_failure:
            return Result.fail(result.error)

        return Result.ok(
            ExportPdfResponse(
                file=result.value,
            )
        )