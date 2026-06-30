from __future__ import annotations

import streamlit as st

from ui.models import BrainState


def render_profile(state: BrainState) -> None:
    profile = state.profile
    aura = profile.aura
    progress = profile.progress

    with st.container(border=True):
        st.markdown("### 👤 Perfil")

        left, right = st.columns(2)

        with left:
            st.text_input(
                "Nombre",
                value=profile.name,
                disabled=True,
            )

            st.metric(
                label="✨ Pureza",
                value=aura.purity,
            )

            st.metric(
                label="🏆 Nivel",
                value=progress.level,
            )

        with right:
            st.metric(
                label="⭐ XP",
                value=progress.xp,
            )

            st.metric(
                label="🎖️ Rango",
                value=progress.rank.value,
            )

            st.progress(
                progress.xp % 100 / 100,
                text=f"{progress.xp % 100}/100 XP",
            )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="🧠 Ánimo",
                value=aura.mood,
            )

        with col2:
            st.metric(
                label="⚡ Energía",
                value=aura.energy,
            )

        with col3:
            st.metric(
                label="🌪️ Caos",
                value=aura.chaos,
            )