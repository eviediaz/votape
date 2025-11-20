import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from src.database import get_db_engine, seed_data

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="VotoClaro 2026",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS (Opcional para mejorar el look) ---
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO (NAVEGACIÓN) ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_candidato_id' not in st.session_state:
    st.session_state.selected_candidato_id = None

def ir_a_home():
    st.session_state.view = 'home'
    st.session_state.selected_candidato_id = None

def ir_a_perfil(candidato_id):
    st.session_state.view = 'perfil'
    st.session_state.selected_candidato_id = candidato_id

# --- FUNCIONES DE CARGA DE DATOS ---
def get_candidatos_data():
    engine = get_db_engine()
    if engine:
        with engine.connect() as conn:
            # 1. Traemos info básica y alertas
            query_candidatos = """
            SELECT c.id, c.nombre, c.partido, c.foto_url, 
                   m.valor as alertas
            FROM candidatos c
            LEFT JOIN metricas m ON c.id = m.candidato_id AND m.tipo_metrica = 'conteo_alertas'
            ORDER BY c.nombre;
            """
            df_candidatos = pd.read_sql(query_candidatos, conn)
            
            # 2. Traemos los temas prioritarios
            query_temas = """
            SELECT candidato_id, detalle_json 
            FROM metricas 
            WHERE tipo_metrica = 'tema_prioritario'
            """
            df_temas = pd.read_sql(query_temas, conn)
            
            # 3. Procesamos los temas para agregarlos al dataframe principal
            # Extraemos el nombre del tema del JSON (ej: {"tema": "Seguridad"} -> "Seguridad")
            if not df_temas.empty:
                df_temas['tema'] = df_temas['detalle_json'].apply(lambda x: x.get('tema', ''))
                # Agrupamos por candidato y creamos una lista de temas: ["Seguridad", "Economía"]
                temas_por_candidato = df_temas.groupby('candidato_id')['tema'].apply(list).reset_index()
                
                # Unimos (Merge) con la tabla de candidatos
                df_final = pd.merge(df_candidatos, temas_por_candidato, left_on='id', right_on='candidato_id', how='left')
            else:
                df_final = df_candidatos
                df_final['tema'] = None # Crear columna vacía si no hay temas
                
            return df_final
    return pd.DataFrame()

def get_detalle_candidato(candidato_id):
    engine = get_db_engine()
    if engine:
        with engine.connect() as conn:
            # Info básica
            candidato = pd.read_sql(text(f"SELECT * FROM candidatos WHERE id = {candidato_id}"), conn).iloc[0]
            # Métricas
            metricas = pd.read_sql(text(f"SELECT * FROM metricas WHERE candidato_id = {candidato_id}"), conn)
            return candidato, metricas
    return None, None

# --- VISTAS (PÁGINAS) ---

def render_home():
    st.title("🇵🇪 VotoClaro 2026")
    # st.markdown("### Monitor Cívico de Inteligencia Artificial")
    
    # with st.expander("🔧 Zona de Desarrollador"):
    #     if st.button("♻️ Resetear Datos con ALERTAS"):
    #         seed_data()
    #         st.rerun()

    # st.divider()
    
    df = get_candidatos_data()
    
    cols = st.columns(3)
    
    for index, row in df.iterrows():
        col = cols[index % 3]
        with col:
            with st.container(border=True):
            # 1. FOTO Y NOMBRE
                st.image(row['foto_url'], use_container_width=True)
                st.subheader(row['nombre'])
                
                # 2. AFILIACIÓN (PARTIDO)
                st.markdown(f"**Afiliación:** {row['partido']}")
                
                # 3. PROPUESTAS PRINCIPALES (TAGS)
                temas = row['tema'] if isinstance(row['tema'], list) else []
                if temas:
                    st.caption("Ejes Clave:")
                    # Creamos un string de HTML para mostrar "chips" o etiquetas bonitas
                    html_tags = ""
                    for tema in temas[:3]: # Mostramos máximo 3 para no saturar
                        html_tags += f"<span style='background-color: #f0f2f6; color: #31333F; padding: 4px 8px; border-radius: 12px; font-size: 12px; margin-right: 4px;'>{tema}</span>"
                    st.markdown(html_tags, unsafe_allow_html=True)
                else:
                    st.caption("Sin ejes definidos aún.")
                
                st.write("") # Espacio vacío
                
                # 4. ALERTAS (SEMÁFORO)
                n_alertas = int(row['alertas']) if pd.notnull(row['alertas']) else 0
                if n_alertas == 0:
                    st.success(f"✅ Sin Alertas")
                elif n_alertas <= 2:
                    st.warning(f"⚠️ {n_alertas} Alertas")
                else:
                    st.error(f"🚨 {n_alertas} Alertas Críticas")
                
                # 5. BOTÓN DE ACCIÓN
                if st.button(f"Ver Perfil Completo ➔", key=f"btn_{row['id']}"):
                    ir_a_perfil(row['id'])
                    st.rerun()

def render_perfil():
    c_id = st.session_state.selected_candidato_id
    candidato, metricas = get_detalle_candidato(c_id)
    
    if st.button("⬅️ Volver a Inicio"):
        ir_a_home()
        st.rerun()
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(candidato['foto_url'])
    with col2:
        st.title(candidato['nombre'])
        st.markdown(f"### {candidato['partido']}")
        st.write(candidato['biografia_resumen'])

    st.divider()
    st.subheader("🔍 Detalles del Candidato")
    
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        st.markdown("#### Historial y Alertas")
        # Filtrar alerta
        alerta_metrica = metricas[metricas['tipo_metrica'] == 'conteo_alertas']
        if not alerta_metrica.empty:
            val = int(alerta_metrica.iloc[0]['valor'])
            detalles = alerta_metrica.iloc[0]['detalle_json'].get('detalle', [])
            
            st.metric("Total Alertas", val)
            if val > 0:
                st.write("Detalle de casos:")
                for caso in detalles:
                    st.warning(f"• {caso}")
            else:
                st.success("No se registran procesos o sentencias mayores en la DB.")
        else:
            st.write("Sin información.")

    with m_col2:
        st.markdown("#### Prioridades del Discurso")
        temas_df = metricas[metricas['tipo_metrica'] == 'tema_prioritario'].copy()
        if not temas_df.empty:
            temas_df['nombre_tema'] = temas_df['detalle_json'].apply(lambda x: x.get('tema', 'Otros'))
            fig_temas = px.pie(temas_df, values='valor', names='nombre_tema', hole=0.4)
            st.plotly_chart(fig_temas, use_container_width=True)
            
# --- CONTROLADOR PRINCIPAL ---
if st.session_state.view == 'home':
    render_home()
elif st.session_state.view == 'perfil':
    render_perfil()