from __future__ import annotations

from copy import deepcopy
from typing import Any

import streamlit as st

from ui.models import BrainState

APP_SESSION_KEY = "pureaura_state"


class SessionManager:
    """
    Single authorized access point for st.session_state.

    This is a Presentation-layer concern because it depends
    on Streamlit's session state mechanism.
    """

    def __init__(self, key: str = APP_SESSION_KEY) -> None:
        self._key = key

    def initialize(self) -> BrainState:
        if self._key not in st.session_state:
            st.session_state[self._key] = BrainState()

        return st.session_state[self._key]

    def get(self) -> BrainState:
        return self.initialize()

    def save(self, state: BrainState) -> None:
        st.session_state[self._key] = state

    def reset(self) -> BrainState:
        state = BrainState()
        st.session_state[self._key] = state
        return state

    def exists(self) -> bool:
        return self._key in st.session_state

    def snapshot(self) -> BrainState:
        return deepcopy(self.get())

    def update(self, **fields: Any) -> BrainState:
        state = self.get()

        for name, value in fields.items():
            if not hasattr(state, name):
                raise AttributeError(
                    f"BrainState has no attribute '{name}'."
                )

            setattr(state, name, value)

        self.save(state)
        return state


session = SessionManager()