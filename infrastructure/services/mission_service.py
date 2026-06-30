from __future__ import annotations

from application.contracts import MissionGenerator
from application.contracts.ai import AIProvider
from domain.result import Result


class MissionService(MissionGenerator):
    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        self._provider = provider

    async def generate(
        self,
        *,
        message: str,
        aura: dict,
    ) -> Result[list[dict], Exception]:
        try:
            response = await self._provider.generate_missions(
                message=message,
                aura=aura,
            )

            return Result.ok(response.missions)

        except Exception as exc:
            return Result.fail(exc)

    async def complete(
        self,
        mission_id: str,
    ) -> Result[dict, Exception]:
        try:
            response = await self._provider.complete_mission(
                mission_id=mission_id,
            )

            return Result.ok(response.mission)

        except Exception as exc:
            return Result.fail(exc)