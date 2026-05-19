import streamlit as st
from groq import Groq
from datetime import date
import re
from fpdf import FPDF  # Recordá tener 'fpdf2' en tu requirements.txt

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL (PureAura by iAgent Solution)
st.set_page_config(page_title="PureAura | iAgent Solution", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    .main-title { 
        color: #10b981; font-size: 5rem; font-weight: 900; 
        text-align: center; margin-bottom: 5px; letter-spacing: -3px; line-height: 0.9;
    }
    .tagline {
        text-align: center; color: #64748b; font-size: 1.4rem; 
        font-weight: 400; margin-bottom: 35px;
    }
    .info-box {
        background: rgba(16, 185, 129, 0.05);
        padding: 20px; border-radius: 20px;
        border-left: 5px solid #10b981;
        margin-bottom: 25px;
    }
    .metric-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px; border-radius: 15px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Contexto y Signo
def obtener_signo(fecha):
    if not fecha: return "No especificado"
    dia, mes = fecha.day, fecha.month
    signos = [(20, "Capricornio"), (19, "Acuario"), (20, "Piscis"), (20, "Aries"), (21, "Tauro"), (21, "Géminis"), (22, "Cáncer"), (22, "Leo"), (23, "Virgo"), (23, "Libra"), (22, "Escorpio"), (21, "Sagitario"), (12, "Capricornio")]
    return signos[mes - 1][1] if dia <= signos[mes - 1][0] else signos[mes][1]

def obtener_estacion_contexto():
    hoy = date.today()
    if hoy.month in [3, 4, 5]: return "Otoño (Fase de transición y ahorro de energía)"
    elif hoy.month in [6, 7, 8]: return "Invierno (Fase de introspección y refuerzo biológico)"
    elif hoy.month in [9, 10, 11]: return "Primavera (Fase de expansión y vitalidad)"
    else: return "Verano (Fase de alto rendimiento y termorregulación)"

# 2. INICIALIZACIÓN ROBUSTA DEL ESTADO DE SESIÓN
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "messages" not in st.session_state: st.session_state.messages = []
if "last_action" not in st.session_state: st.session_state.last_action = None
if "valores_db" not in st.session_state: st.session_state.valores_db = {"Energía": 5, "Estrés": 5, "Foco": 5}
if "user_data" not in st.session_state: st.session_state.user_data = None

# 3. PANTALLA DE ACCESO
if not st.session_state.autenticado or st.session_state.user_data is None:
    st.session_state.autenticado = False
    
    st.markdown('<p class="main-title">PureAura</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Purificá el caos, dominá tu ritmo</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box">
            <b>🎯 Tip de precisión:</b> No es necesario cargar todas las opciones, pero cuanto más info reciba <b>PureAura</b>, 
            más acertadas y personalizadas serán las respuestas.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        nombre = st.text_input("¿Cómo te llamamos?*", placeholder="Tu nombre o Nick")
        concepto = st.text_input("Autopercepción actual (Opcional)", placeholder="¿Cómo te sentís hoy?")
        sexo = st.radio("Género (Opcional)", ["Masculino", "Femenino", "Prefiero omitir"], index=2, horizontal=True)
    with col2:
        avatar = st.selectbox("Arquetipo visual (Opcional)", ["Neutro", "🥷 Ninja", "🤖 Robot", "👨‍🚀 Astronauta", "🦄 Unicornio"])
        nac_check = st.checkbox("Incluir mi Signo (Cargar fecha)")
        fecha_nac = st.date_input("Fecha de nacimiento", value=date(2000, 1, 1)) if nac_check else None

    st.write("---")
    if st.button("🚀 Iniciar Escaneo de Aura"):
        if nombre:
            st.session_state.user_data = {
                "nombre": nombre, "concepto": concepto if concepto else "Neutro",
                "sexo": sexo, "avatar": avatar, "signo": obtener_signo(fecha_nac) if fecha_nac else "No especificado",
                "estacion": obtener_estacion_contexto()
            }
            st.session_state.autenticado = True
            st.rerun()
        else: 
            st.error("⚠️ Necesitamos al menos tu nombre para arrancar.")

# 4. DASHBOARD Y CHAT
else:
    u = st.session_state.user_data
    with st.sidebar:
        st.title("✨ PureAura")
        st.caption("by @iagentsolution")
        st.write(f"👤 {u['nombre']}")
        st.write(f"🔮 Signo: {u['signo']}")
        st.divider()
        
        # Conexión automática: Prioriza secrets, evita que quede vacío si la app duerme
        secret_key = st.secrets.get("GROQ_API_KEY", "")
        api_key = st.text_input("Groq API Key (Admin)", type="password", value=secret_key)
        
        if st.button("Finalizar Sesión"):
            st.session_state.clear()
            st.rerun()

    st.markdown("### 📊 Estado de tu Aura")
    c1, c2, c3 = st.columns(3)
    with c1:
        e = st.session_state.valores_db["Energía"]
        st.markdown(f"<div class='metric-box'>⚡ Energía<br><h2>{e}/10</h2></div>", unsafe_allow_html=True)
        st.progress(e/10)
    with c2:
        s = st.session_state.valores_db["Estrés"]
        st.markdown(f"<div class='metric-box'>🚨 Estrés<br><h2>{s}/10</h2></div>", unsafe_allow_html=True)
        st.progress(s/10)
    with c3:
        f = st.session_state.valores_db["Foco"]
        st.markdown(f"<div class='metric-box'>🎯 Foco<br><h2>{f}/10</h2></div>", unsafe_allow_html=True)
        st.progress(f/10)

    st.divider()

    if not st.session_state.messages:
        st.write("### ¿Dónde enfocamos el análisis hoy?")
        b1, b2, b3 = st.columns(3)
        with b1: 
            if st.button("🍎 Cuerpo y Nutrición"): st.session_state.last_action = "Evaluar mi estado físico y alimentación."
        with b2:
            if st.button("🚭 Hábitos y Rutinas"): st.session_state.last_action = "Analizar mis hábitos y descanso."
        with b3:
            if st.button("🧠 Estrategia Mental"): st.session_state.last_action = "Optimizar mi foco y manejo de ansiedad."

    # Renderizado seguro de mensajes anteriores
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])

    def llamar_ia(mensajes):
        if not api_key: 
            return "⚠️ Falta la API Key de Groq. Configurala en los Secrets de Streamlit o en la barra lateral.", None
        try:
            client = Groq(api_key=api_key)
            system = f"Sos PureAura de @iagentsolution. Analizás a {u['nombre']}, {u['sexo']}, signo {u['signo']}. Autopercepción: {u['concepto']}. Contexto estacional: {u['estacion']}. Usá metáforas de su arquetipo ({u['avatar']}). Al final incluí métricas en un único bloque exacto al final del mensaje: [E:X, S:Y, F:Z] donde X, Y y Z sean números enteros del 1 al 10."
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": system}] + mensajes, temperature=0.7)
            raw = res.choices[0].message.content
            
            match = re.search(r"\[E:(\d+),\s*S:(\d+),\s*F:(\d+)\]", raw)
            mets = {"Energía": int(match.group(1)), "Estrés": int(match.group(2)), "Foco": int(match.group(3))} if match else None
            
            clean_txt = re.sub(r"\[E:\d+,\s*S:\d+,\s*F:\d+\]", "", raw).strip()
            return clean_txt, mets
        except Exception as error: 
            return f"⚠️ Error al conectar con el servidor de IA: {str(error)}", None

    user_input = st.chat_input("Escribí acá...")
    prompt = user_input or st.session_state.last_action
    
    if prompt:
        st.session_state.last_action = None
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            txt, mets = llamar_ia(st.session_state.messages)
            st.markdown(txt)
            if mets: 
                st.session_state.valores_db = mets
        
        st.session_state.messages.append({"role": "assistant", "content": txt})
        st.rerun()

    # FUNCION DE EXPORTACIÓN A PDF CORREGIDA PARA FPDF2
    if len(st.session_state.messages) >= 4:
        st.divider()
        
        # Definimos la función que arma el PDF en memoria para fpdf2
        def generar_pdf_bytes():
            pdf = FPDF()
            pdf.add_page()
            
            # Encabezado principal
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, "PureAura | iAgent Solution", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 10, f"Fecha del Reporte: {date.today()}", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.ln(5)
            
            # Datos del Usuario
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, f"Diagnostico para: {u['nombre']}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Signo: {u['signo']} | Contexto: {u['estacion']}", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 6, f"Métricas actuales -> Energía: {e}/10 | Estrés: {s}/10 | Foco: {f}/10", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)
            
            # Transcripción de la conversación (Controlando tildes y saltos de línea largos)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Historial de Análisis:", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            
            for msg in st.session_state.messages:
                role_label = "Tú" if msg["role"] == "user" else "PureAura"
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, f"[{role_label}]:", new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_font("Helvetica", "", 10)
                # Reemplazamos caracteres conflictivos para evitar errores de codificación latin-1
                texto_limpio = msg["content"].encode('latin-1', 'replace').decode('latin-1')
                
                # multi_cell calcula automáticamente los saltos de línea del texto de la IA
                pdf.multi_cell(0, 5, texto_limpio, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)
                
            return pdf.output() # fpdf2 por defecto devuelve bytes si no especificás archivo

        # Generador directo en el download_button de Streamlit para evitar recargas raras
        try:
            pdf_data = generar_pdf_bytes()
            st.download_button(
                label="📥 Descargar Diagnóstico (.PDF)",
                data=pdf_data,
                file_name=f"PureAura_{u['nombre']}.pdf",
                mime="application/pdf"
            )
        except Exception as e_pdf:
            st.error(f"Error al estructurar el PDF: {e_pdf}")