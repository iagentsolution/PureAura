from __future__ import annotations

from application.contracts import AuraAnalyzer, MessageGenerator
from application.contracts.ai import AIProvider
from domain.result import Result


class AuraService(
    AuraAnalyzer,
    MessageGenerator,
):
    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        self._provider = provider

    async def send_message(
        self,
        message: str,
    ) -> Result:
        try:
            response = await self._provider.send_message(
                message,
            )
            return Result.ok(response)
        except Exception as exc:
            return Result.fail(exc)

    async def analyze(
        self,
        message: str,
    ) -> Result:
        try:
            response = await self._provider.analyze_aura(
                message=message,
            )

            return Result.ok(response.aura)

        except Exception as exc:
            return Result.fail(exc)

    async def analyze_aura(
        self,
        message: str,
    ) -> Result:
        return await self.analyze(message)

    async def generate_message(
        self,
        message: str,
    ) -> Result:
        try:
            response = await self._provider.generate_message(
                message,
            )
            return Result.ok(response)
        except Exception as exc:
            return Result.fail(exc)