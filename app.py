import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Datos Simulados (Simulando la salida de la IA/Base de Datos) ---

# Métrica IA: Foco Temático (Valores normalizados de 0 a 100)
CANDIDATOS_DATA = {
    "Carlos Álvarez": {
        "partido": "Unión por la Gente",
        "foto_url": "https://placehold.co/150x150/4ade80/000000?text=C.A.",
        "Integridad": 75,
        "Seguridad": 90,
        "Educación": 50,
        "Economía": 65,
        "Salud": 40,
        "Propuesta Clave": "Inversión masiva en tecnología educativa."
    },
    "Sofía Torres": {
        "partido": "Frente de la Esperanza",
        "foto_url": "https://placehold.co/150x150/fde047/000000?text=S.T.",
        "Integridad": 95,
        "Seguridad": 40,
        "Educación": 85,
        "Economía": 70,
        "Salud": 60,
        "Propuesta Clave": "Reforma total del sistema de salud pública."
    },
    "Ricardo Gómez": {
        "partido": "Nuevo País",
        "foto_url": "https://placehold.co/150x150/f43f5e/000000?text=R.G.",
        "Integridad": 60,
        "Seguridad": 70,
        "Educación": 60,
        "Economía": 90,
        "Salud": 55,
        "Propuesta Clave": "Reducción de impuestos para impulsar PyMEs."
    }
}

# Métricas Detalladas para la Comparación
METRICAS_COMPARACION = {
    "Carlos Álvarez": {"Denuncias": 15, "Sanciones": 2, "Experiencia Política": "12 años"},
    "Sofía Torres": {"Denuncias": 3, "Sanciones": 0, "Experiencia Política": "4 años"},
    "Ricardo Gómez": {"Denuncias": 8, "Sanciones": 1, "Experiencia Política": "8 años"}
}

# --- Funciones de Visualización ---

def crear_diagrama_arana(candidatos_nombres):
    """Crea un Diagrama de Araña comparando las métricas de los candidatos seleccionados."""
    if not candidatos_nombres:
        return go.Figure()

    fig = go.Figure()
    categories = ['Integridad', 'Seguridad', 'Educación', 'Economía', 'Salud']

    for name in candidatos_nombres:
        data = CANDIDATOS_DATA.get(name)
        if data:
            values = [data[c] for c in categories]
            # Plotly requiere cerrar el ciclo para el diagrama de araña
            values.append(values[0])
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=name,
                hovertemplate=name + '<br>%{theta}: %{r}<extra></extra>'
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title='Foco Temático y Prioridades (0-100)',
        height=500
    )
    return fig

def mostrar_modulo_perfil(candidato_nombre):
    """Muestra la vista detallada del Perfil del Candidato (Módulo 2)."""
    data = CANDIDATOS_DATA.get(candidato_nombre)
    if not data:
        st.error("Candidato no encontrado.")
        return

    st.header(f"Candidato: {candidato_nombre}")
    st.subheader(data["partido"])

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(data["foto_url"], width=120, caption="Hoja de Vida Oficial")
    with col2:
        st.metric("Propuesta Central", data["Propuesta Clave"])
        st.markdown("**Métricas IA (Resumen de Foco Temático):**")

    st.divider()

    # Gráficos Interactivos (Diagrama de Araña)
    st.markdown("#### 📊 Foco Temático (La Métrica IA)")
    fig = crear_diagrama_arana([candidato_nombre])
    st.plotly_chart(fig, use_container_width=True)

    # Chatbot (Exploración de Discurso)
    st.markdown("#### 💬 Chatbot: Exploración de Discurso")
    with st.container(border=True):
        st.markdown("_Pregunta sobre lo que dice el candidato... (Simulación de Chatbot)_")
        pregunta = st.selectbox(
            "Selecciona una pregunta de ejemplo:",
            ["¿Cuál es su plan para la educación?", "¿Cómo abordará la seguridad?", "¿Qué dice sobre la economía?"],
            key=f"chat_{candidato_nombre}"
        )
        if pregunta:
            # Simulación de respuesta de IA (siempre una cita con fuente)
            st.info(f"""
            **Respuesta (Cita Textual):**
            *"{candidato_nombre} afirmó: 'Mi plan para la {pregunta.split()[-1].replace('?', '').lower()} se centra en la descentralización y el uso de tecnologías emergentes para garantizar la calidad en cada rincón del país.'"*
            
            **Fuente:** Entrevista Canal N, 23/Oct/2024.
            """)

    # Llamada a la Acción
    st.markdown("---")
    if st.button("Comparar con otro candidato", type="primary"):
        st.session_state.current_page = 'comparacion'
        st.session_state.candidato_base = candidato_nombre
        st.rerun()

def mostrar_modulo_comparacion(candidato_base=None):
    """Muestra la Vista de Comparación (Módulo 3)."""
    st.title("⚖️ Vista de Comparación (La Decisión)")

    candidatos_disponibles = list(CANDIDATOS_DATA.keys())
    default_cands = []
    if candidato_base and candidato_base in candidatos_disponibles:
        default_cands.append(candidato_base)

    # Selector de Candidatos
    candidatos_seleccionados = st.multiselect(
        "Selecciona 2 o 3 candidatos a comparar (siempre incluye las métricas IA):",
        options=candidatos_disponibles,
        default=default_cands[:3],
        max_selections=3
    )

    if len(candidatos_seleccionados) < 2:
        st.warning("Selecciona al menos dos candidatos para activar la comparación.")
        return

    # Visualización Principal (Diagrama de Araña)
    st.markdown("#### 🕷️ Diagrama de Araña: Foco Temático Comparado")
    fig = crear_diagrama_arana(candidatos_seleccionados)
    st.plotly_chart(fig, use_container_width=True)

    # Resultados Detallados (Tabla Frente a Frente)
    st.markdown("#### 📋 Resultados Detallados: Frente a Frente")
    
    comparacion_df = pd.DataFrame(index=METRICAS_COMPARACION["Carlos Álvarez"].keys())
    
    for cand in candidatos_seleccionados:
        data = METRICAS_COMPARACION.get(cand, {})
        # Añadir las métricas IA de Foco Temático a la comparación
        for metric in ['Integridad', 'Seguridad', 'Educación', 'Economía', 'Salud']:
            data[metric + ' (IA)'] = CANDIDATOS_DATA[cand][metric]
            
        series = pd.Series(data)
        comparacion_df[cand] = series
    
    # Reordenar las filas para que las métricas de IA vayan primero
    ia_metrics = [m + ' (IA)' for m in ['Integridad', 'Seguridad', 'Educación', 'Economía', 'Salud']]
    other_metrics = list(METRICAS_COMPARACION[candidatos_seleccionados[0]].keys())
    new_order = ia_metrics + other_metrics

    # Asegurarse de que las métricas de IA estén al inicio
    final_df = comparacion_df.reindex(new_order)
    
    # Estilos básicos para la tabla
    st.dataframe(
        final_df,
        use_container_width=True,
        # Aplicar estilos básicos para resaltar (ej. menor Denuncias es mejor)
        column_config={
            "Denuncias": st.column_config.NumberColumn(
                "Denuncias / Sanciones",
                help="Total de denuncias o sanciones (menor es mejor)",
                format="%d",
            )
        }
    )

    # Análisis de Discurso Comparado (Innovación)
    st.markdown("#### ✨ Análisis de Discurso Comparado (Innovación Simulación)")
    if len(candidatos_seleccionados) == 2:
        cand_a, cand_b = candidatos_seleccionados
        st.info(f"""
        **Análisis IA sobre el tema 'Seguridad':**
        
        * **Palabras Clave exclusivas de {cand_a}:** "Mano Dura", "Ejército", "Cero Tolerancia".
        * **Palabras Clave exclusivas de {cand_b}:** "Inclusión", "Oportunidades", "Prevención Social".
        
        *(Simulación de una herramienta que extrae las diferencias de léxico, reflejando enfoques opuestos: represión vs. prevención.)*
        """)
    else:
        st.info("Selecciona exactamente dos candidatos para ver el análisis de discurso comparado.")

def mostrar_home():
    """Muestra la vista inicial del Home (Módulo 1)."""
    st.title("💡 VotoClaro IA: Decisiones Informadas")
    st.markdown("#### Centraliza, analiza y compara candidatos políticos.")
    
    # Entrada del Usuario (Barra de Búsqueda)
    st.markdown("---")
    st.markdown("### 🔍 Flujo Central: Búsqueda y Comparación")
    
    input_text = st.text_input(
        "Escribe un nombre o una pregunta para empezar:",
        placeholder="Ej.: 'Carlos Álvarez' o '¿Quién se enfoca más en Seguridad?'"
    )

    if input_text:
        # Lógica de la IA (Simulación)
        
        # Opción A: Búsqueda Directa por Nombre
        if any(c.lower() in input_text.lower() for c in CANDIDATOS_DATA.keys()):
            # La IA identifica un nombre de candidato
            candidato_encontrado = next(c for c in CANDIDATOS_DATA.keys() if c.lower() in input_text.lower())
            st.session_state.current_page = 'perfil'
            st.session_state.candidato_base = candidato_encontrado
            st.success(f"Opción A: Reconocido '{candidato_encontrado}'. Saltando al Perfil.")
            st.rerun()

        # Opción B: Búsqueda Comparativa/Agregada por Pregunta
        elif "?" in input_text or "quién" in input_text.lower():
            # La IA identifica una pregunta comparativa
            st.success("Opción B: Pregunta Agregada detectada. Saltando a la Vista de Comparación.")
            
            # Simulamos el resultado de la IA ordenando por métrica (Ej.: 'Seguridad')
            metric_order = "Seguridad" # Asumimos la métrica más probable

            st.info(f"*(Simulación: La IA ordena por la métrica solicitada, en este caso, '{metric_order}')*")
            
            candidatos_ordenados = sorted(
                CANDIDATOS_DATA.items(), 
                key=lambda item: item[1].get(metric_order, 0), 
                reverse=True
            )
            
            st.markdown(f"**Resultado de la Métrica '{metric_order}' (Más a Menos Foco):**")
            for name, data in candidatos_ordenados:
                st.markdown(f"- **{name}:** {data[metric_order]}% de Foco Temático.")

            if st.button("Ver Comparación Detallada", key="go_compare_home", type="primary"):
                # Establece los dos primeros como base para la comparación
                top_cands = [name for name, _ in candidatos_ordenados[:2]]
                st.session_state.current_page = 'comparacion'
                st.session_state.candidato_base = top_cands[0] if top_cands else None
                st.rerun()
            
        else:
            st.warning("No se encontró un candidato ni una pregunta clara. Intenta un nombre (Ej: Carlos Álvarez) o una pregunta (Ej: ¿Quién se enfoca más en Educación?).")


# --- Control Principal de la Aplicación (Rutas) ---

# Inicializar el estado de la sesión para manejar las páginas
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'candidato_base' not in st.session_state:
    st.session_state.candidato_base = None

# Barra de Navegación Simple
with st.sidebar:
    st.image("https://placehold.co/150x50/1d4ed8/ffffff?text=VotoClaro+IA")
    st.header("Navegación")
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.candidato_base = None
        st.rerun()
        
    if st.session_state.current_page == 'perfil' and st.session_state.candidato_base:
        if st.button(f"👤 Perfil: {st.session_state.candidato_base}", use_container_width=True):
            st.rerun()
            
    if st.button("⚖️ Comparación", use_container_width=True):
        st.session_state.current_page = 'comparacion'
        st.rerun()

# Renderizar la página actual
if st.session_state.current_page == 'home':
    mostrar_home()
elif st.session_state.current_page == 'perfil' and st.session_state.candidato_base:
    mostrar_modulo_perfil(st.session_state.candidato_base)
elif st.session_state.current_page == 'comparacion':
    # Pasa el candidato base si existe para precargar la selección en el multiselect
    mostrar_modulo_comparacion(st.session_state.candidato_base)
else:
    # Fallback al Home si el estado es inconsistente
    mostrar_home()
