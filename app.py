from __future__ import annotations

import streamlit as st

from application.container import Container
from brain import Brain
from ui.chat import render_chat
from ui.login import render_login
from ui.profile import render_profile
from ui.session import session
from ui.sidebar import render_sidebar
from ui.styles import apply_styles


def main() -> None:
    st.set_page_config(
        page_title="PureAura",
        layout="wide",
    )

    apply_styles()

    state = session.initialize()

    if "_container" not in st.session_state:
        container = Container()
        st.session_state["_container"] = container
        st.session_state["_brain"] = Brain(
            send_message=container.send_message,
            analyze_aura=container.analyze_aura,
            generate_missions=container.generate_missions,
            complete_mission=container.complete_mission,
            update_progress=container.update_progress,
            export_pdf=container.export_pdf,
        )

    render_login()

    render_sidebar(state)

    render_profile(state)

    render_chat(state)


if __name__ == "__main__":
    main()