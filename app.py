import streamlit as st
from groq import Groq

st.set_page_config(page_title="PureAura | iAgent Solution", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #10b981; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    .footer { text-align: center; margin-top: 50px; color: #64748b; font-size: 14px; }
    .footer a { color: #10b981; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "perfil_creado" not in st.session_state:
    st.session_state.perfil_creado = False

def llamar_ia(mensajes, nombre, avatar):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    system_prompt = {
        "role": "system",
        "content": (f"Sos PureAura de @iagentsolution. Usuario: {nombre}, Estilo: {avatar}. "
                    "Tu objetivo es ser un asistente de alto rendimiento. Sé conciso y motivador. "
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
        return "Servicio temporalmente ocupado. Por favor, intenta de nuevo en unos instantes."

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
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
            
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
            st.rerun()

st.markdown("""
    <div class="footer">
        <p>✨ <b>PureAura</b> es un desarrollo exclusivo de <a href="https://www.instagram.com/iagentsolution" target="_blank">@iagentsolution</a></p>
        <p>Potenciando negocios con Agentes de Inteligencia Artificial a medida.</p>
    </div>
    """, unsafe_allow_html=True)