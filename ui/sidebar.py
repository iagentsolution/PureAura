from __future__ import annotations

import streamlit as st

from ui.models import BrainState


def _metric(label: str, value: int) -> None:
    st.metric(label=label, value=f"{value}")


def _mission_completed(mission: object) -> bool:
    if isinstance(mission, dict):
        return bool(mission.get("completed", False))

    completed = getattr(mission, "completed", False)

    if callable(completed):
        return bool(completed())

    return bool(completed)


def _mission_value(mission: object, field: str, default=None):
    if isinstance(mission, dict):
        return mission.get(field, default)

    return getattr(mission, field, default)


def render_sidebar(state: BrainState) -> None:
    profile = state.profile
    aura = profile.aura
    progress = profile.progress

    with st.sidebar:
        st.markdown("## ✨ PureAura")
        st.caption("Sistema operativo de bienestar")

        st.divider()

        st.subheader(profile.name)

        st.progress(progress.xp % 100 / 100)

        st.caption(
            f"Nivel {progress.level} • {progress.rank.value}"
        )

        st.divider()

        _metric("🧠 Ánimo", aura.mood)
        _metric("⚡ Energía", aura.energy)
        _metric("🌪️ Caos", aura.chaos)
        _metric("✨ Pureza", aura.purity)

        st.divider()

        st.subheader("Misiones")

        if not state.missions:
            st.caption("No hay misiones disponibles.")

        for mission in state.missions:
            status = "✅" if _mission_completed(mission) else "⬜"

            title = _mission_value(mission, "title", "")
            description = _mission_value(
                mission,
                "description",
                "",
            )
            xp_reward = _mission_value(
                mission,
                "xp_reward",
                0,
            )

            st.markdown(
                f"""
**{status} {title}**

{description}

**+{xp_reward} XP**
"""
            )