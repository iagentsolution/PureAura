from __future__ import annotations

import streamlit as st


def render_login() -> bool:
    """
    Renderiza una pantalla de bienvenida.
    Devuelve True cuando el usuario decide ingresar.

    Esta implementación es intencionalmente stateless para permitir
    reemplazarla posteriormente por autenticación real (OAuth, Clerk,
    Auth0, Supabase Auth, etc.) sin afectar al resto del sistema.
    """

    left, center, right = st.columns([1, 1.4, 1])

    with center:
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
<div style="text-align:center">
    <h1>✨ PureAura</h1>
    <p>
        Sistema operativo de bienestar,
        claridad mental y productividad.
    </p>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("")

        st.text_input(
            "Nombre",
            placeholder="¿Cómo querés que te llame?",
            key="login_name",
        )

        st.text_input(
            "Correo electrónico (opcional)",
            placeholder="nombre@email.com",
            key="login_email",
        )

        st.markdown("")

        return st.button(
            "Comenzar",
            use_container_width=True,
            type="primary",
        )