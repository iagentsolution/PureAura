from __future__ import annotations

from application.contracts import PdfExporter
from domain.result import Result


class PdfService(PdfExporter):
    async def export(
        self,
        *,
        profile: dict,
        aura: dict,
        missions: list[dict],
        progress: dict,
    ) -> Result[bytes, Exception]:
        try:
            pdf = await self._build_pdf(
                profile=profile,
                aura=aura,
                missions=missions,
                progress=progress,
            )
            return Result.ok(pdf)
        except Exception as exc:
            return Result.fail(exc)

    async def _build_pdf(
        self,
        *,
        profile: dict,
        aura: dict,
        missions: list[dict],
        progress: dict,
    ) -> bytes:
        content = [
            "PUREAURA REPORT",
            "",
            f"PROFILE: {profile}",
            f"AURA: {aura}",
            f"MISSIONS: {missions}",
            f"PROGRESS: {progress}",
        ]

        return "\n".join(content).encode("utf-8")