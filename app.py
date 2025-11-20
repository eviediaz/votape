import streamlit as st
from src.database import get_db_engine, seed_data
from sqlalchemy import text
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="VotoClaro MVP", layout="wide")

st.title("🏛️ VotoClaro IA - Panel de Control MVP")

# --- SECCIÓN DE DEBUG / SETUP ---
with st.expander("⚙️ Administración de Datos (Solo Dev)"):
    st.warning("Usa este botón para reiniciar la base de datos con información de prueba.")
    if st.button("♻️ Resetear y Sembrar Datos de Prueba"):
        seed_data()

st.divider()

# --- SECCIÓN DE VISUALIZACIÓN PRELIMINAR ---
st.subheader("🔍 Vista Rápida de la Base de Datos")

engine = get_db_engine()
if engine:
    try:
        with engine.connect() as conn:
            # Traer candidatos
            candidatos = pd.read_sql("SELECT * FROM candidatos", conn)
            
            if not candidatos.empty:
                st.write(f"Se encontraron **{len(candidatos)}** candidatos:")
                st.dataframe(candidatos)
                
                # Ejemplo de visualización rápida (Si ya ejecutaste el botón de arriba)
                st.markdown("### 📊 Ejemplo de Gráfico Rápido")
                metricas = pd.read_sql("""
                    SELECT c.nombre, m.valor 
                    FROM metricas m 
                    JOIN candidatos c ON m.candidato_id = c.id 
                    WHERE m.tipo_metrica = 'sentimiento_promedio'
                """, conn)
                
                if not metricas.empty:
                    st.bar_chart(metricas, x="nombre", y="valor", color="#FF4B4B")
                    st.caption("Sentimiento Promedio (0 = Negativo, 1 = Positivo)")
            else:
                st.info("La base de datos está vacía. ¡Dale al botón de arriba para cargar datos!")
                
    except Exception as e:
        st.error(f"Error leyendo datos: {e}")