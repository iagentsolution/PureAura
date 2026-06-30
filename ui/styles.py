from __future__ import annotations

import streamlit as st


_GLOBAL_CSS = """
<style>
:root{
    --bg:#F7F8FC;
    --surface:#FFFFFF;
    --surface-2:#F2F4F8;
    --border:#E6EAF2;
    --text:#171A21;
    --muted:#6F7785;
    --accent:#5B7CFA;
    --radius:18px;
    --shadow:0 10px 30px rgba(15,23,42,.06);
}

html, body, [data-testid="stAppViewContainer"]{
    background:var(--bg);
    color:var(--text);
}

[data-testid="stHeader"]{
    background:transparent;
}

[data-testid="stSidebar"]{
    background:var(--surface);
    border-right:1px solid var(--border);
}

.block-container{
    max-width:1200px;
    padding-top:1.5rem;
    padding-bottom:2rem;
}

div[data-testid="stChatMessage"]{
    border:1px solid var(--border);
    border-radius:var(--radius);
    background:var(--surface);
    box-shadow:var(--shadow);
    padding:.35rem;
}

div[data-testid="stChatInput"]{
    padding-top:1rem;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    border:1px solid var(--border);
    background:var(--surface);
}

.stButton>button:hover{
    border-color:var(--accent);
}

hr{
    border-color:var(--border);
}

.pa-title{
    font-size:1.7rem;
    font-weight:700;
    margin-bottom:.15rem;
}

.pa-subtitle{
    color:var(--muted);
    margin-bottom:1.25rem;
}

.pa-card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    box-shadow:var(--shadow);
}
</style>
"""


def apply_styles() -> None:
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)