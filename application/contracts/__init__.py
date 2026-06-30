from __future__ import annotations

from abc import ABC, abstractmethod

from domain.result import Result


class MessageGenerator(ABC):
    @abstractmethod
    async def send_message(
        self,
        message: str,
    ) -> Result:
        raise NotImplementedError


class AuraAnalyzer(ABC):
    @abstractmethod
    async def analyze(
        self,
        message: str,
    ) -> Result:
        raise NotImplementedError


class MissionGenerator(ABC):
    @abstractmethod
    async def generate(
        self,
        *,
        message: str,
        aura: dict,
    ) -> Result:
        raise NotImplementedError

    @abstractmethod
    async def complete(
        self,
        mission_id: str,
    ) -> Result:
        raise NotImplementedError


class ProgressTracker(ABC):
    @abstractmethod
    def update(
        self,
        *,
        message: str,
        aura: dict,
        missions: list[dict],
    ) -> Result:
        raise NotImplementedError

    @abstractmethod
    def reward(
        self,
        mission: dict,
    ) -> Result:
        raise NotImplementedError


class PdfExporter(ABC):
    @abstractmethod
    async def export(
        self,
        *,
        profile: dict,
        aura: dict,
        missions: list[dict],
        progress: dict,
    ) -> Result:
        raise NotImplementedError