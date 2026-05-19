[19/5/26 6:47 p. m.] Elsa Vandija: import streamlit as st
from groq import Groq
from datetime import date
import re
from fpdf import FPDF

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
st.set_page_config(page_title="PureAura | iAgent Solution", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #10b981; font-size: 5.5rem; font-weight: 900; text-align: center; margin-bottom: 0px; letter-spacing: -4px; line-height: 1; }
    .tagline { text-align: center; color: #64748b; font-size: 1.5rem; font-weight: 400; margin-bottom: 40px; }
    .metric-box { background: rgba(16, 185, 129, 0.08); padding: 15px; border-radius: 15px; border: 1px solid rgba(16, 185, 129, 0.2); text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Lógicas de apoyo
def obtener_estacion():
    mes = date.today().month
    if mes in [3, 4, 5]: return "Otoño"
    elif mes in [6, 7, 8]: return "Invierno"
    elif mes in [9, 10, 11]: return "Primavera"
    else: return "Verano"

# 2. ESTADO DE SESIÓN
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "messages" not in st.session_state: st.session_state.messages = []
if "valores_db" not in st.session_state: st.session_state.valores_db = {"Energía": 5, "Estrés": 5, "Foco": 5}
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nombre": "", "avatar": "Neutro", "estacion": obtener_estacion()}

# 3. PANTALLA DE ACCESO
if not st.session_state.autenticado:
    st.markdown('<p class="main-title">PureAura</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Purificá el caos, dominá tu ritmo</p>', unsafe_allow_html=True)
    col_c, _ = st.columns([1, 1])
    with col_c:
        nombre_i = st.text_input("¿Cómo te llamás?", placeholder="Tu nombre...")
        if st.button("🚀 Iniciar Escaneo"):
            if nombre_i:
                st.session_state.user_data["nombre"] = nombre_i
                st.session_state.autenticado = True
                st.rerun()

# 4. CHAT Y DASHBOARD
else:
    u = st.session_state.user_data
    
    # --- BARRA LATERAL ---
    with st.sidebar:
        st.title("✨ Status")
        e, s, f = st.session_state.valores_db.values()
        st.markdown(f"<div class='metric-box'>⚡ E: {e} | 🚨 S: {s} | 🎯 F: {f}</div>", unsafe_allow_html=True)
        st.divider()
        u["avatar"] = st.selectbox("Arquetipo", ["Neutro", "⚡ High Performer", "🌿 Zen", "🛡️ Estoico", "🎮 Gamer", "🔥 Urban"])
        if st.button("Nueva Sesión"):
            st.session_state.clear()
            st.rerun()

    # --- CUERPO DEL CHAT ---
    st.markdown(f"### Hola, {u['nombre']}")
    
    if not st.session_state.messages:
        st.info("👋 ¿En qué nos enfocamos hoy? ¿Rutina, alimentación, algún problema con un emprendimiento o simplemente optimizar tu foco?")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # Función PDF con marca iAgent Solution
    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        # Marca de agua / Encabezado
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 5, "@iagentsolution - Inteligencia Artificial Personalizada", ln=True, align="R")
        
        pdf.ln(10)
        pdf.set_text_color(16, 185, 129) # Verde PureAura
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 10, "Plan de Acción PureAura", ln=True, align="L")
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, f"Preparado para: {u['nombre']} | Fecha: {date.today()}", ln=True)
        pdf.cell(0, 10, f"Métricas finales del Aura: Energía {e}/10 | Estrés {s}/10 | Foco {f}/10", ln=True)
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
[19/5/26 6:47 p. m.] Elsa Vandija: for m in st.session_state.messages:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(100, 100, 100)
            role = "USUARIO" if m["role"] == "user" else "PUREAURA"
            pdf.cell(0, 8, f"{role}:", ln=True)
            
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            texto = m["content"].encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 5, texto)
            pdf.ln(2)
        
        # Pie de página con firma
        pdf.ln(10)
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 10, "Este plan fue generado por una IA personalizada de @iagentsolution.", align="C")
        return pdf.output()

    def llamar_ia(mensajes):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system = (f"Sos PureAura de @iagentsolution. Usuario: {u['nombre']}, Arquetipo: {u['avatar']}. "
                  "Si el usuario parece haber resuelto su duda o finalizado el plan, cerrá con calidez "
                  "y menciónale que puede descargar su plan en PDF con el botón que aparecerá. "
                  "Al final de CADA mensaje incluí: [E:X, S:Y, F:Z]")
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":system}] + mensajes)
        raw = res.choices[0].message.content
        match = re.search(r"\[E:(\d+),\s*S:(\d+),\s*F:(\d+)\]", raw)
        mets = {"Energía": int(match.group(1)), "Estrés": int(match.group(2)), "Foco": int(match.group(3))} if match else None
        return re.sub(r"\[E:\d+,\s*S:\d+,\s*F:\d+\]", "", raw).strip(), mets

    user_input = st.chat_input("¿Qué hay en tu mente?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(user_input)
        with st.chat_message("assistant"):
            txt, mets = llamar_ia(st.session_state.messages)
            st.markdown(txt)
            if mets: st.session_state.valores_db = mets
            # MOSTRAR BOTÓN DE PDF SOLO DESPUÉS DE LA RESPUESTA
            st.download_button(label="📥 Descargar mi Plan PureAura (.pdf)", 
                             data=generar_pdf(), 
                             file_name=f"Plan_PureAura_{u['nombre']}.pdf", 
                             mime="application/pdf")
        st.session_state.messages.append({"role": "assistant", "content": txt})
        st.rerun()