import streamlit as st
import pandas as pd
import google.generativeai as genai
from src.database import get_db_engine

st.set_page_config(page_title="Asistente IA Real", page_icon="🧠")

# 1. CONFIGURAR GOOGLE GEMINI
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Falta la GOOGLE_API_KEY en secrets.toml")

def buscar_y_responder_con_gemini(pregunta):
    engine = get_db_engine()
    if not engine: return "Error de DB"

    # A. OBTENER DATOS (CONTEXTO)
    with engine.connect() as conn:
        query = "SELECT contenido, tema, c.nombre, c.partido FROM propuestas p JOIN candidatos c ON p.candidato_id = c.id"
        df = pd.read_sql(query, conn)
        
    # Convertimos todo el dataframe a un texto largo para que la IA lo lea
    contexto_texto = ""
    for _, row in df.iterrows():
        contexto_texto += f"- Candidato {row['nombre']} ({row['partido']}) sobre {row['tema']}: '{row['contenido']}'\n"

    # B. CREAR EL PROMPT PARA GEMINI (RAG)
    # Aquí le damos la orden estricta de NO inventar.
    prompt_sistema = f"""
    Eres un asistente cívico neutral para las elecciones de Perú.
    Usa SOLO la siguiente información oficial para responder la pregunta del usuario.
    Si la respuesta no está en el texto, di "No tengo información oficial sobre eso".
    No des tu opinión. Cita al candidato.

    INFORMACIÓN OFICIAL:
    {contexto_texto}

    PREGUNTA DEL USUARIO:
    {pregunta}
    """

    # C. GENERAR RESPUESTA
    try:
        model = genai.GenerativeModel('gemini-flash-latest') # Modelo rápido y gratis
        response = model.generate_content(prompt_sistema)
        return response.text
    except Exception as e:
        return f"Error consultando a Gemini: {e}"

# --- INTERFAZ ---
st.title("Asistente Cívico")
st.caption("Potenciado por Google AI Studio. Las respuestas son generadas por IA basándose estrictamente en la base de datos.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hola. Soy una IA que lee los planes de gobierno. ¿Qué quieres saber?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ej: ¿Quién propone penas más duras?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Leyendo planes de gobierno con IA..."):
            respuesta_ai = buscar_y_responder_con_gemini(prompt)
            st.markdown(respuesta_ai)
            
    st.session_state.messages.append({"role": "assistant", "content": respuesta_ai})