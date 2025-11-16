import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# --- Datos Simulados (Simulando la salida de la IA/Base de Datos) ---

# Métrica IA: Foco Temático (Valores normalizados de 0 a 100)
CANDIDATOS_DATA = {
    "Carlos Perez": {
        "partido": "Unión por la Gente",
        "foto_url": "https://placehold.co/150x150/4ade80/000000?text=C.A.",
        "Integridad": 75,
        "Seguridad": 90,
        "Educación": 50,
        "Economía": 65,
        "Salud": 40,
        "Propuesta Clave": "Inversión masiva en tecnología educativa.",
        "region": "Nacional",
        "edad": 52,
        "ocupacion_actual": "Diputado"
    },
    "Sofía Torres": {
        "partido": "Frente de la Esperanza",
        "foto_url": "https://placehold.co/150x150/fde047/000000?text=S.T.",
        "Integridad": 95,
        "Seguridad": 40,
        "Educación": 85,
        "Economía": 70,
        "Salud": 60,
        "Propuesta Clave": "Reforma total del sistema de salud pública.",
        "region": "Urbano",
        "edad": 38,
        "ocupacion_actual": "Senadora"
    },
    "Ricardo Gómez": {
        "partido": "Nuevo País",
        "foto_url": "https://placehold.co/150x150/f43f5e/000000?text=R.G.",
        "Integridad": 60,
        "Seguridad": 70,
        "Educación": 60,
        "Economía": 90,
        "Salud": 55,
        "Propuesta Clave": "Reducción de impuestos para impulsar PyMEs.",
        "region": "Rural",
        "edad": 45,
        "ocupacion_actual": "Empresario"
    }
}

# Métricas Detalladas para la Comparación
METRICAS_COMPARACION = {
    "Carlos Perez": {
        "Denuncias": 15,
        "Sanciones": 2,
        "Experiencia Política": "12 años",
        "Promesas Cumplidas": "65%",
        "Credibilidad IA": 72,
        "Última Actualización": "2025-11-15"
    },
    "Sofía Torres": {
        "Denuncias": 3,
        "Sanciones": 0,
        "Experiencia Política": "4 años",
        "Promesas Cumplidas": "88%",
        "Credibilidad IA": 91,
        "Última Actualización": "2025-11-16"
    },
    "Ricardo Gómez": {
        "Denuncias": 8,
        "Sanciones": 1,
        "Experiencia Política": "8 años",
        "Promesas Cumplidas": "72%",
        "Credibilidad IA": 78,
        "Última Actualización": "2025-11-14"
    }
}

# Base de Conocimiento Simulada (Citas y Discursos por Tema)
BASE_CONOCIMIENTO = {
    "Carlos Perez": {
        "Educación": [
            {"texto": "La educación es la base del progreso. Invertiremos en tecnología en cada aula.", "fuente": "Debate Presidencial Canal N", "fecha": "2025-10-23", "confiabilidad": "Alta"},
            {"texto": "Necesitamos llevar internet de calidad a las zonas rurales.", "fuente": "Conferencia de Prensa", "fecha": "2025-11-10", "confiabilidad": "Alta"}
        ],
        "Seguridad": [
            {"texto": "Aumentaremos la presencia policial en zonas de riesgo.", "fuente": "Propuesta de Gobierno", "fecha": "2025-11-01", "confiabilidad": "Media"},
            {"texto": "Implementaremos sistemas de vigilancia inteligente.", "fuente": "Entrevista Exclusiva", "fecha": "2025-10-15", "confiabilidad": "Media"}
        ],
        "Economía": [
            {"texto": "Apoyaremos a las pequeñas empresas con créditos accesibles.", "fuente": "Plan Económico Oficial", "fecha": "2025-09-20", "confiabilidad": "Alta"}
        ]
    },
    "Sofía Torres": {
        "Salud": [
            {"texto": "Reforma integral del sistema de salud con énfasis en atención primaria.", "fuente": "Plataforma Electoral", "fecha": "2025-11-05", "confiabilidad": "Alta"},
            {"texto": "Acceso universal a medicamentos esenciales sin costo.", "fuente": "Propuesta Sanitaria", "fecha": "2025-10-30", "confiabilidad": "Alta"}
        ],
        "Educación": [
            {"texto": "Aumentar inversión en educación al 8% del PIB.", "fuente": "Debate Presidencial", "fecha": "2025-10-23", "confiabilidad": "Alta"},
            {"texto": "Becas completas para estudiantes de bajos recursos.", "fuente": "Comunicado Oficial", "fecha": "2025-11-02", "confiabilidad": "Alta"}
        ]
    },
    "Ricardo Gómez": {
        "Economía": [
            {"texto": "Reduciremos los impuestos corporativos del 30% al 20%.", "fuente": "Plan Fiscal", "fecha": "2025-11-08", "confiabilidad": "Media"},
            {"texto": "Eliminaremos regulaciones que inhiben el crecimiento empresarial.", "fuente": "Entrevista Económica", "fecha": "2025-10-25", "confiabilidad": "Media"}
        ],
        "Seguridad": [
            {"texto": "Mayor inversión en tecnología policial y capacitación.", "fuente": "Propuesta de Seguridad", "fecha": "2025-11-01", "confiabilidad": "Media"}
        ]
    }
}

# Verificación de Información Simulada
VERIFICACIONES = {
    "Carlos Perez": {
        "credibilidad_general": 72,
        "fuentes_verificadas": 8,
        "declaraciones_verificadas": 12,
        "promesas_cumplidas": "65%",
        "promesas_incumplidas": "22%",
        "promesas_en_progreso": "13%"
    },
    "Sofía Torres": {
        "credibilidad_general": 91,
        "fuentes_verificadas": 15,
        "declaraciones_verificadas": 22,
        "promesas_cumplidas": "88%",
        "promesas_incumplidas": "4%",
        "promesas_en_progreso": "8%"
    },
    "Ricardo Gómez": {
        "credibilidad_general": 78,
        "fuentes_verificadas": 10,
        "declaraciones_verificadas": 18,
        "promesas_cumplidas": "72%",
        "promesas_incumplidas": "15%",
        "promesas_en_progreso": "13%"
    }
}

# --- Funciones Auxiliares de IA Simulada ---

def obtener_respuesta_chatbot(candidato_nombre, tema):
    """Simula respuestas de IA basadas en base de conocimiento."""
    conocimiento = BASE_CONOCIMIENTO.get(candidato_nombre, {}).get(tema, [])
    
    if not conocimiento:
        return None
    
    # Selecciona aleatoriamente una cita de la base de conocimiento
    cita = random.choice(conocimiento)
    return cita

def get_color_credibilidad(score):
    """Retorna color basado en puntuación de credibilidad."""
    if score >= 85:
        return "🟢"  # Verde - Alta
    elif score >= 70:
        return "🟡"  # Amarillo - Media
    else:
        return "🔴"  # Rojo - Baja

def get_label_confiabilidad(score):
    """Retorna etiqueta de confiabilidad."""
    if score >= 85:
        return "Alta"
    elif score >= 70:
        return "Media"
    else:
        return "Baja"

def verificar_informacion(candidato_nombre):
    """Retorna análisis de verificación de información."""
    return VERIFICACIONES.get(candidato_nombre, {})

def buscar_candidatos_por_filtros(tema=None, region=None, experiencia_min=None):
    """Filtra candidatos por tema, región y experiencia."""
    resultados = []
    
    for nombre, datos in CANDIDATOS_DATA.items():
        # Filtro por tema (métrica IA)
        if tema and tema not in datos:
            continue
        if tema and datos[tema] < 60:  # Tema no es fortaleza
            continue
            
        # Filtro por región
        if region and datos.get("region", "").lower() != region.lower():
            continue
            
        # Filtro por experiencia
        if experiencia_min:
            exp_years = int(METRICAS_COMPARACION[nombre]["Experiencia Política"].split()[0])
            if exp_years < experiencia_min:
                continue
        
        resultados.append(nombre)
    
    return resultados

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
        
        # Información Personal
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Edad", data["edad"])
        with col_info2:
            st.metric("Ocupación Actual", data["ocupacion_actual"])
        with col_info3:
            st.metric("Región", data["region"])

    st.divider()

    # --- Sección de Verificación de Información ---
    st.markdown("### ✅ Verificación de Información")
    verificacion = verificar_informacion(candidato_nombre)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        credibilidad_score = verificacion.get("credibilidad_general", 0)
        color = get_color_credibilidad(credibilidad_score)
        st.metric(f"{color} Credibilidad IA", f"{credibilidad_score}%")
    with col2:
        st.metric("Fuentes Verificadas", verificacion.get("fuentes_verificadas", 0))
    with col3:
        st.metric("Promesas Cumplidas", verificacion.get("promesas_cumplidas", "N/A"))
    with col4:
        st.metric("Declaraciones Verificadas", verificacion.get("declaraciones_verificadas", 0))
    
    # Desglose de promesas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"✅ Cumplidas: {verificacion.get('promesas_cumplidas', 'N/A')}")
    with col2:
        st.warning(f"⏳ En Progreso: {verificacion.get('promesas_en_progreso', 'N/A')}")
    with col3:
        st.error(f"❌ Incumplidas: {verificacion.get('promesas_incumplidas', 'N/A')}")

    st.divider()

    # Gráficos Interactivos (Diagrama de Araña)
    st.markdown("#### 📊 Foco Temático (La Métrica IA)")
    fig = crear_diagrama_arana([candidato_nombre])
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Chatbot Mejorado (Exploración de Discurso)
    st.markdown("#### 💬 Chatbot: Exploración de Discurso Verificado")
    with st.container(border=True):
        st.markdown("_Pregunta sobre lo que dice el candidato (respuestas basadas en información verificada)_")
        
        # Selector de tema
        temas_disponibles = list(BASE_CONOCIMIENTO.get(candidato_nombre, {}).keys())
        if not temas_disponibles:
            st.warning("No hay información verificada disponible para este candidato.")
        else:
            tema_seleccionado = st.selectbox(
                "Selecciona un tema para explorar:",
                temas_disponibles,
                key=f"tema_{candidato_nombre}"
            )
            
            if tema_seleccionado:
                # Obtener respuesta de la "IA"
                respuesta = obtener_respuesta_chatbot(candidato_nombre, tema_seleccionado)
                
                if respuesta:
                    # Mostrar respuesta con verificación
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"""
                        **Declaración sobre {tema_seleccionado}:**
                        
                        *"{respuesta['texto']}"*
                        
                        **Fuente:** {respuesta['fuente']} ({respuesta['fecha']})
                        """)
                    with col2:
                        confiabilidad = respuesta.get('confiabilidad', 'Media')
                        if confiabilidad == 'Alta':
                            st.success(f"🟢 {confiabilidad}")
                        elif confiabilidad == 'Media':
                            st.warning(f"🟡 {confiabilidad}")
                        else:
                            st.error(f"🔴 {confiabilidad}")

    st.divider()

    # Llamada a la Acción
    if st.button("Comparar con otro candidato", type="primary"):
        st.session_state.current_page = 'comparacion'
        st.session_state.candidato_base = candidato_nombre
        st.rerun()

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

    # --- Búsqueda Avanzada ---
    st.markdown("### 🔍 Búsqueda Avanzada")
    with st.expander("Filtros Avanzados", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tema_filtro = st.selectbox(
                "Filtrar por Fortaleza Temática:",
                ["Todos", "Integridad", "Seguridad", "Educación", "Economía", "Salud"],
                key="tema_filtro"
            )
        
        with col2:
            region_filtro = st.selectbox(
                "Filtrar por Región:",
                ["Todos", "Nacional", "Urbano", "Rural"],
                key="region_filtro"
            )
        
        with col3:
            experiencia_filtro = st.selectbox(
                "Experiencia Mínima:",
                [0, 4, 8, 12],
                key="exp_filtro"
            )
        
        # Aplicar filtros
        tema_param = tema_filtro if tema_filtro != "Todos" else None
        region_param = region_filtro if region_filtro != "Todos" else None
        exp_param = experiencia_filtro if experiencia_filtro > 0 else None
        
        candidatos_filtrados = buscar_candidatos_por_filtros(tema_param, region_param, exp_param)
        
        if candidatos_filtrados:
            st.success(f"✅ {len(candidatos_filtrados)} candidato(s) encontrado(s)")
            candidatos_disponibles = candidatos_filtrados
        else:
            st.warning("No se encontraron candidatos con los filtros seleccionados.")
            candidatos_disponibles = list(CANDIDATOS_DATA.keys())

    st.divider()

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

    # --- Sección de Credibilidad ---
    st.markdown("#### 🛡️ Análisis de Credibilidad Comparado")
    credibilidad_df = pd.DataFrame({
        candidato: {
            "Credibilidad IA": VERIFICACIONES[candidato]["credibilidad_general"],
            "Promesas Cumplidas": VERIFICACIONES[candidato]["promesas_cumplidas"],
            "Fuentes Verificadas": VERIFICACIONES[candidato]["fuentes_verificadas"]
        }
        for candidato in candidatos_seleccionados
    }).T
    
    st.dataframe(credibilidad_df, use_container_width=True)

    # Resultados Detallados (Tabla Frente a Frente)
    st.markdown("#### 📋 Resultados Detallados: Frente a Frente")
    
    comparacion_df = pd.DataFrame(index=METRICAS_COMPARACION["Carlos Perez"].keys())
    
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
    
    st.dataframe(
        final_df,
        use_container_width=True,
        column_config={
            "Denuncias": st.column_config.NumberColumn(
                "Denuncias",
                help="Total de denuncias (menor es mejor)",
                format="%d",
            )
        }
    )

    # Análisis de Discurso Comparado (Innovación)
    st.markdown("#### ✨ Análisis de Discurso Comparado")
    if len(candidatos_seleccionados) == 2:
        cand_a, cand_b = candidatos_seleccionados
        
        # Temas en común
        temas_cand_a = set(BASE_CONOCIMIENTO.get(cand_a, {}).keys())
        temas_cand_b = set(BASE_CONOCIMIENTO.get(cand_b, {}).keys())
        temas_comunes = temas_cand_a & temas_cand_b
        
        if temas_comunes:
            st.info(f"""
            **Análisis Comparativo de Discurso:**
            
            **Temas Comunes:** {', '.join(temas_comunes)}
            
            **Fortalezas Únicas de {cand_a}:** {', '.join(temas_cand_a - temas_cand_b) if temas_cand_a - temas_cand_b else 'Ninguna'}
            
            **Fortalezas Únicas de {cand_b}:** {', '.join(temas_cand_b - temas_cand_a) if temas_cand_b - temas_cand_a else 'Ninguna'}
            """)
            
            # Comparación de credibilidad en tema común
            if temas_comunes:
                tema_selec = st.selectbox("Analizar tema común:", list(temas_comunes))
                
                cita_a = obtener_respuesta_chatbot(cand_a, tema_selec)
                cita_b = obtener_respuesta_chatbot(cand_b, tema_selec)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**{cand_a}:**")
                    if cita_a:
                        st.markdown(f"*{cita_a['texto']}*")
                        st.caption(f"Confiabilidad: {cita_a['confiabilidad']}")
                with col2:
                    st.markdown(f"**{cand_b}:**")
                    if cita_b:
                        st.markdown(f"*{cita_b['texto']}*")
                        st.caption(f"Confiabilidad: {cita_b['confiabilidad']}")
        else:
            st.info("No hay temas comunes entre estos candidatos en la base de conocimiento.")
    else:
        st.info("Selecciona exactamente dos candidatos para ver el análisis de discurso comparado detallado.")

def mostrar_home():
    """Muestra la vista inicial del Home (Módulo 1)."""
    st.title("💡 VotoClaro IA: Decisiones Informadas")
    st.markdown("#### Centraliza, analiza y compara candidatos políticos con información verificada.")
    
    # Entrada del Usuario (Barra de Búsqueda)
    st.markdown("---")
    st.markdown("### 🔍 Flujo Central: Búsqueda y Comparación")
    
    input_text = st.text_input(
        "Escribe un nombre o una pregunta para empezar:",
        placeholder="Ej.: 'Carlos Perez' o '¿Quién se enfoca más en Seguridad?'"
    )

    if input_text:
        # Lógica de la IA (Simulación)
        
        # Opción A: Búsqueda Directa por Nombre
        if any(c.lower() in input_text.lower() for c in CANDIDATOS_DATA.keys()):
            # La IA identifica un nombre de candidato
            candidato_encontrado = next(c for c in CANDIDATOS_DATA.keys() if c.lower() in input_text.lower())
            st.session_state.current_page = 'perfil'
            st.session_state.candidato_base = candidato_encontrado
            st.success(f"✅ Reconocido '{candidato_encontrado}'. Saltando al Perfil.")
            st.rerun()

        # Opción B: Búsqueda Comparativa/Agregada por Pregunta
        elif "?" in input_text or "quién" in input_text.lower():
            # La IA identifica una pregunta comparativa
            st.success("✅ Pregunta Agregada detectada. Análisis en progreso...")
            
            # Detectar métrica probable de la pregunta
            temas = ['Seguridad', 'Educación', 'Economía', 'Salud', 'Integridad']
            metric_order = "Seguridad"  # Default
            
            for tema in temas:
                if tema.lower() in input_text.lower():
                    metric_order = tema
                    break

            st.info(f"🔎 **La IA detectó**: Búsqueda por métrica '{metric_order}'")
            
            candidatos_ordenados = sorted(
                CANDIDATOS_DATA.items(), 
                key=lambda item: item[1].get(metric_order, 0), 
                reverse=True
            )
            
            st.markdown(f"**Resultado ordenado por '{metric_order}' (Mayor a Menor Foco):**")
            
            # Mostrar resultados con credibilidad
            for idx, (name, data) in enumerate(candidatos_ordenados, 1):
                credibilidad = VERIFICACIONES[name]["credibilidad_general"]
                color = get_color_credibilidad(credibilidad)
                st.markdown(
                    f"{idx}. **{name}** - {data[metric_order]}% | {color} Credibilidad: {credibilidad}%"
                )

            if st.button("Ver Comparación Detallada", key="go_compare_home", type="primary"):
                top_cands = [name for name, _ in candidatos_ordenados[:2]]
                st.session_state.current_page = 'comparacion'
                st.session_state.candidato_base = top_cands[0] if top_cands else None
                st.rerun()
            
        else:
            st.warning("❌ No se encontró un candidato ni una pregunta clara. Intenta un nombre (Ej: Carlos Perez) o una pregunta (Ej: ¿Quién se enfoca más en Educación?).")

    # Mostrar candidatos destacados
    st.markdown("---")
    st.markdown("### ⭐ Candidatos Destacados")
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (name, data) in enumerate(CANDIDATOS_DATA.items()):
        col = [col1, col2, col3][idx]
        with col:
            credibilidad = VERIFICACIONES[name]["credibilidad_general"]
            color = get_color_credibilidad(credibilidad)
            
            st.markdown(f"### {name}")
            st.image(data["foto_url"], width=120)
            st.markdown(f"**Partido:** {data['partido']}")
            st.markdown(f"**Propuesta:** {data['Propuesta Clave']}")
            st.markdown(f"{color} **Credibilidad:** {credibilidad}%")
            
            if st.button(f"Ver Perfil de {name}", key=f"btn_{name}"):
                st.session_state.current_page = 'perfil'
                st.session_state.candidato_base = name
                st.rerun()


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
