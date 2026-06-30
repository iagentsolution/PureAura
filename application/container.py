from __future__ import annotations

from application.analyze_aura import AnalyzeAuraUseCase
from application.complete_mission import CompleteMissionUseCase
from application.contracts.ai import AIProvider
from application.export_pdf import ExportPdfUseCase
from application.generate_missions import GenerateMissionsUseCase
from application.send_message import SendMessageUseCase
from application.update_progress import UpdateProgressUseCase
from infrastructure.ai.factory import create_ai_provider
from infrastructure.services.aura_service import AuraService
from infrastructure.services.mission_service import MissionService
from infrastructure.services.pdf_service import PdfService
from infrastructure.services.xp_service import XpService


class Container:
    def __init__(
        self,
        provider: AIProvider | None = None,
    ) -> None:
        self._provider = provider

        self._aura_service: AuraService | None = None
        self._mission_service: MissionService | None = None
        self._pdf_service: PdfService | None = None
        self._xp_service: XpService | None = None

        self._send_message: SendMessageUseCase | None = None
        self._analyze_aura: AnalyzeAuraUseCase | None = None
        self._generate_missions: GenerateMissionsUseCase | None = None
        self._complete_mission: CompleteMissionUseCase | None = None
        self._update_progress: UpdateProgressUseCase | None = None
        self._export_pdf: ExportPdfUseCase | None = None

    @property
    def provider(self) -> AIProvider:
        if self._provider is None:
            self._provider = create_ai_provider()

        return self._provider

    @property
    def aura_service(self) -> AuraService:
        if self._aura_service is None:
            self._aura_service = AuraService(self.provider)

        return self._aura_service

    @property
    def mission_service(self) -> MissionService:
        if self._mission_service is None:
            self._mission_service = MissionService(self.provider)

        return self._mission_service

    @property
    def pdf_service(self) -> PdfService:
        if self._pdf_service is None:
            self._pdf_service = PdfService()

        return self._pdf_service

    @property
    def xp_service(self) -> XpService:
        if self._xp_service is None:
            self._xp_service = XpService()

        return self._xp_service

    @property
    def send_message(self) -> SendMessageUseCase:
        if self._send_message is None:
            self._send_message = SendMessageUseCase(
                message_generator=self.aura_service,
                aura_analyzer=self.aura_service,
                mission_generator=self.mission_service,
                progress_tracker=self.xp_service,
            )

        return self._send_message

    @property
    def analyze_aura(self) -> AnalyzeAuraUseCase:
        if self._analyze_aura is None:
            self._analyze_aura = AnalyzeAuraUseCase(
                aura_analyzer=self.aura_service,
            )

        return self._analyze_aura

    @property
    def generate_missions(self) -> GenerateMissionsUseCase:
        if self._generate_missions is None:
            self._generate_missions = GenerateMissionsUseCase(
                mission_generator=self.mission_service,
            )

        return self._generate_missions

    @property
    def complete_mission(self) -> CompleteMissionUseCase:
        if self._complete_mission is None:
            self._complete_mission = CompleteMissionUseCase(
                mission_generator=self.mission_service,
                progress_tracker=self.xp_service,
            )

        return self._complete_mission

    @property
    def update_progress(self) -> UpdateProgressUseCase:
        if self._update_progress is None:
            self._update_progress = UpdateProgressUseCase(
                progress_tracker=self.xp_service,
            )

        return self._update_progress

    @property
    def export_pdf(self) -> ExportPdfUseCase:
        if self._export_pdf is None:
            self._export_pdf = ExportPdfUseCase(
                pdf_exporter=self.pdf_service,
            )

        return self._export_pdf