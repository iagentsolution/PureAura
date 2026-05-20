import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PureAura | iAgent Solution", page_icon="✨", layout="centered")

# Estilo CSS para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #10b981; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE SESIÓN ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "perfil_creado" not in st.session_state:
    st.session_state.perfil_creado = False

# --- FUNCIONES ---
def limpiar_texto(texto):
    """Elimina o reemplaza caracteres que FPDF no puede renderizar en fuentes estándar"""
    # FPDF nativo no se lleva bien con emojis. Esto evita que rompa el PDF.
    return texto.encode('ascii', 'ignore').decode('ascii')

def generar_pdf(nombre, avatar, historial):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado con tu marca
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(16, 185, 129) # Verde iAgent
    pdf.cell(0, 10, "iAgent Solution - Plan Personalizado", ln=True, align='C')
    
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"PureAura: Tu Asistente IA | Fecha: {datetime.date.today()}", ln=True, align='C')
    pdf.ln(10)
    
    # Datos del Usuario
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Usuario: {limpiar_texto(nombre)}", ln=True)
    pdf.cell(0, 10, f"Enfoque: {avatar}", ln=True)
    pdf.ln(5)
    
    # Contenido del Chat
    for msg in historial:
        role = "Tu" if msg["role"] == "user" else "PureAura"
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(0, 10, f"{role}:")
        pdf.set_font("Arial", '', 11)
        
        # Limpiamos el contenido para que no rompa por emojis o formatos raros
        texto_limpio = limpiar_texto(msg["content"])
        pdf.multi_cell(0, 10, texto_limpio)
        pdf.ln(2)
        
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    pdf.multi_cell(0, 10, "Gracias por confiar en iAgent Solution. Para soluciones empresariales o agentes a medida, contactanos via Instagram @iagentsolution.")
    
    # Retorna los bytes directamente (Compatible con fpdf y fpdf2)
    return pdf.output()

def llamar_ia(mensajes, nombre, avatar):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # System prompt con el gancho de ventas sutil al final
    system_prompt = {
        "role": "system",
        "content": (f"Sos PureAura de @iagentsolution. Usuario: {nombre}, Estilo: {avatar}. "
                    "Tu objetivo es ser un asistente de alto rendimiento. Sé conciso y motivador. "
                    "Si el usuario parece haber terminado, recordale que puede descargar el PDF con su plan. "
                    "Menciona sutilmente que iAgent Solution crea agentes personalizados para negocios si el contexto lo permite.")
    }
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[system_prompt] + mensajes,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("✨ PureAura")
st.subheader("Tu próximo paso, guiado por IA.")

if not st.session_state.perfil_creado:
    with st.container():
        st.write("Configurá tu asistente para comenzar:")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("¿Cómo te llamás?", placeholder="Tu nombre")
        with col2:
            avatar = st.selectbox("Elegí tu arquetipo:", ["Estoico", "Productivo/Negocios", "Zen/Salud", "Gamer/Directo"])
        
        if st.button("Comenzar Experiencia"):
            if nombre:
                st.session_state.user_data = {"nombre": nombre, "avatar": avatar}
                st.session_state.perfil_creado = True
                st.rerun()
            else:
                st.warning("Por favor, ingresá tu nombre.")

else:
    # Mostrar Historial
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
            
    # Input del Chat
    if prompt := st.chat_input("¿En qué trabajamos hoy?"):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            respuesta = llamar_ia(
                st.session_state.mensajes, 
                st.session_state.user_data["nombre"], 
                st.session_state.user_data["avatar"]
            )
            st.markdown(respuesta)
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            st.rerun() # Fuerza el refresco para actualizar el estado del botón de descarga

    # --- BOTÓN DE DESCARGA ---
    if len(st.session_state.mensajes) > 0:
        st.divider()
        try:
            pdf_bytes = generar_pdf(
                st.session_state.user_data["nombre"], 
                st.session_state.user_data["avatar"], 
                st.session_state.mensajes
            )
            st.download_button(
                label="📥 Descargar mi Plan en PDF",
                data=bytes(pdf_bytes), # Nos aseguramos de pasarle un objeto de bytes puro
                file_name=f"Plan_PureAura_{st.session_state.user_data['nombre']}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Hubo un problema al generar el PDF: {e}")