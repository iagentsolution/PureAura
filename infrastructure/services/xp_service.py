from __future__ import annotations

from application.contracts import ProgressTracker
from domain.result import Result


class XpService(ProgressTracker):
    def update(
        self,
        *,
        message: str,
        aura: dict,
        missions: list[dict],
    ) -> Result[dict, Exception]:
        try:
            progress = {
                "xp": 0,
                "level": 1,
                "missions_generated": len(missions),
            }

            return Result.ok(progress)

        except Exception as exc:
            return Result.fail(exc)

    def reward(
        self,
        mission: dict,
    ) -> Result[dict, Exception]:
        try:
            xp_reward = mission.get("xp_reward", 0)

            progress = {
                "xp_gained": xp_reward,
            }

            return Result.ok(progress)

        except Exception as exc:
            return Result.fail(exc)