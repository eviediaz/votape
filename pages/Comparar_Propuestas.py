import streamlit as st
import pandas as pd
from src.database import get_db_engine

# Configuración de página
st.set_page_config(page_title="Comparador - VotoClaro", page_icon="🔎")

# --- LÓGICA DE BASE DE DATOS ---
def get_todas_propuestas():
    engine = get_db_engine()
    if engine:
        with engine.connect() as conn:
            query = """
            SELECT p.contenido, p.tema, p.fuente_url, 
                   c.nombre as candidato_nombre, c.foto_url, c.partido
            FROM propuestas p
            JOIN candidatos c ON p.candidato_id = c.id
            """
            return pd.read_sql(query, conn)
    return pd.DataFrame()

def calcular_similitud(query, propuestas_df):
    # Simulación simple de similitud (MVP)
    query_words = set(query.lower().split())
    scores = []
    for texto in propuestas_df['contenido']:
        texto_lower = texto.lower()
        coincidencias = sum(1 for word in query_words if word in texto_lower)
        score = coincidencias * 10 
        scores.append(score)
    propuestas_df['score_similitud'] = scores
    return propuestas_df.sort_values(by='score_similitud', ascending=False)

# --- INICIALIZAR ESTADO DEL BUSCADOR ---
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# Función para actualizar el buscador desde los botones
def set_query(texto):
    st.session_state.search_query = texto

# --- INTERFAZ ---
st.title("🔎 Comparador de Propuestas")
st.markdown("Describe una problemática o selecciona un tema rápido:")

# === 🆕 SECCIÓN DE BOTONES RÁPIDOS (DEFAULT) ===
st.markdown("##### Temas Sugeridos")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("👮 Seguridad", use_container_width=True):
        set_query("construcción de cárceles seguridad delincuencia mano dura")
with col2:
    if st.button("💰 Economía", use_container_width=True):
        set_query("apoyo pymes economia creditos empleo")
with col3:
    if st.button("📜 Constitución", use_container_width=True):
        set_query("reforma constitución pena de muerte corrupción")
with col4:
    if st.button("🏥 Salud", use_container_width=True):
        set_query("sistema de salud hospitales atención médica")
# ===============================================

# 1. Input del Usuario (Conectado al session_state)
query = st.text_area(
    "Tu búsqueda:", 
    value=st.session_state.search_query, # Aquí toma el valor del botón
    placeholder="Ej: Quiero mano dura contra la delincuencia...", 
    height=100,
    key="input_busqueda" # Clave única
)

# Sincronizar el cambio manual del usuario con el estado
if query != st.session_state.search_query:
    st.session_state.search_query = query

buscar_btn = st.button("Buscar Coincidencias", type="primary")

# 2. Lógica de Búsqueda (Se activa con el botón Buscar O si hay texto precargado por los botones)
if buscar_btn or st.session_state.search_query:
    
    # Solo buscamos si hay algo escrito
    if st.session_state.search_query.strip():
        with st.spinner("Analizando propuestas..."):
            df_propuestas = get_todas_propuestas()
            
            if not df_propuestas.empty:
                # Usamos el texto del session_state
                resultados = calcular_similitud(st.session_state.search_query, df_propuestas)
                top_resultados = resultados[resultados['score_similitud'] > 0].head(5)
                
                st.divider()
                st.subheader("Resultados Encontrados")
                
                if top_resultados.empty:
                    st.warning("No encontramos coincidencias exactas. Intenta con palabras más generales.")
                else:
                    for idx, row in top_resultados.iterrows():
                        with st.container(border=True):
                            col_img, col_texto = st.columns([1, 4])
                            with col_img:
                                st.image(row['foto_url'], width=80)
                            with col_texto:
                                st.markdown(f"### {row['candidato_nombre']} ({row['partido']})")
                                st.caption(f"Tema: {row['tema']}")
                                st.info(f"📜 \"{row['contenido']}\"")
                                st.markdown(f"[🔗 Ver Fuente]({row['fuente_url']})")
                                st.progress(min(row['score_similitud'] * 10, 100) / 100)
            else:
                st.error("Base de datos vacía.")