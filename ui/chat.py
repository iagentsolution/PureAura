from __future__ import annotations

import streamlit as st

from domain.message import MessageRole
from ui.models import BrainState


_PAGE_TITLE = "✨ PureAura"
_PAGE_SUBTITLE = (
    "Tu sistema operativo de bienestar, claridad mental y productividad."
)


def _render_header() -> None:
    st.markdown(
        f"""
<div class="pa-title">{_PAGE_TITLE}</div>
<div class="pa-subtitle">{_PAGE_SUBTITLE}</div>
""",
        unsafe_allow_html=True,
    )


def _render_history(state: BrainState) -> None:
    for message in state.chat_history:
        avatar = "🧑" if message.role is MessageRole.USER else "✨"

        with st.chat_message(
            name=message.role.value,
            avatar=avatar,
        ):
            st.markdown(message.content)


def render_chat(state: BrainState) -> str | None:
    _render_header()
    _render_history(state)

    return st.chat_input(
        "Escribí lo que necesitás..."
    )