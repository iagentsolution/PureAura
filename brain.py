from __future__ import annotations

from application.analyze_aura import (
    AnalyzeAuraRequest,
    AnalyzeAuraUseCase,
)
from application.complete_mission import (
    CompleteMissionRequest,
    CompleteMissionUseCase,
)
from application.export_pdf import (
    ExportPdfRequest,
    ExportPdfUseCase,
)
from application.generate_missions import (
    GenerateMissionsRequest,
    GenerateMissionsUseCase,
)
from application.send_message import (
    SendMessageRequest,
    SendMessageUseCase,
)
from application.update_progress import (
    UpdateProgressRequest,
    UpdateProgressUseCase,
)


class Brain:
    def __init__(
        self,
        send_message: SendMessageUseCase,
        analyze_aura: AnalyzeAuraUseCase,
        generate_missions: GenerateMissionsUseCase,
        complete_mission: CompleteMissionUseCase,
        update_progress: UpdateProgressUseCase,
        export_pdf: ExportPdfUseCase,
    ) -> None:
        self._send_message = send_message
        self._analyze_aura = analyze_aura
        self._generate_missions = generate_missions
        self._complete_mission = complete_mission
        self._update_progress = update_progress
        self._export_pdf = export_pdf

    async def send_message(self, message: str):
        return await self._send_message.execute(
            SendMessageRequest(message=message)
        )

    async def analyze_aura(self, message: str):
        return await self._analyze_aura.execute(
            AnalyzeAuraRequest(message=message)
        )

    async def generate_missions(self, message, aura):
        return await self._generate_missions.execute(
            GenerateMissionsRequest(
                message=message,
                aura=aura,
            )
        )

    async def complete_mission(self, mission_id: str):
        return await self._complete_mission.execute(
            CompleteMissionRequest(
                mission_id=mission_id,
            )
        )

    async def update_progress(
        self,
        message,
        aura,
        missions,
    ):
        return await self._update_progress.execute(
            UpdateProgressRequest(
                message=message,
                aura=aura,
                missions=missions,
            )
        )

    async def export_pdf(
        self,
        profile,
        aura,
        missions,
        progress,
    ):
        return await self._export_pdf.execute(
            ExportPdfRequest(
                profile=profile,
                aura=aura,
                missions=missions,
                progress=progress,
            )
        )