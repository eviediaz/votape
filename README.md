# 🗳️ VotoClaro 2026

**Acceso amigable e interactivo a la información de las elecciones**, es una plataforma que democratiza el conocimiento sobre propuestas de candidatos mediante IA, comparadores inteligentes y análisis cívico. El proyecto está disponible en https://votape.streamlit.app/

## 📋 Descripción del Proyecto

VotoClaro es una aplicación web desarrollada con **Streamlit** que transforma la forma en que los ciudadanos acceden a información electoral. La plataforma utiliza inteligencia artificial y análisis de datos para hacer más comprensible y accesible el panorama político, permitiendo:

- **Visualización intuitiva** de candidatos y sus propuestas
- **Búsqueda inteligente** de propuestas por tema o problemática
- **Asistente cívico con IA** que responde preguntas sobre planes de gobierno
- **Comparación dinámica** entre candidatos y sus posiciones
- **Análisis automatizado** de sentimiento y temas prioritarios

La aplicación está diseñada para ciudadanos sin experiencia técnica que quieren entender las opciones electorales de forma rápida y confiable.

## 🎯 Características

- 📊 **Dashboard**: Galería de candidatos con métricas, sentimientos y perfiles
- 🤖 **Asistente IA**: Chat con Gemini que responde preguntas sobre propuestas
- 🔎 **Comparador**: Búsqueda inteligente de propuestas por tema
- 📈 **Análisis**: Visualización de temas prioritarios y sentimientos

## 🏗️ Stack Tecnológico

- **Frontend/Backend**: Streamlit + Python 3.9+
- **Base de Datos**: PostgreSQL + SQLAlchemy
- **IA**: Google Gemini API (RAG)
- **Visualización**: Plotly Express, Pandas

### Estructura

```
votape/
├── app.py                     # Dashboard principal
├── pages/
│   ├── Asistente_IA.py       # Chat cívico
│   └── Comparar_Propuestas.py # Buscador
├── src/database.py            # Conexión BD
└── requirements.txt
```

## 🚀 Instalación Rápida

**Requisitos**: Python 3.9+, PostgreSQL 12+, API key Gemini

```bash
# 1. Clonar y configurar
git clone <repository-url> && cd votape
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configurar .streamlit/secrets.toml
# [connections.postgresql]
# host = "localhost"
# port = 5432
# database = "votape_db"
# username = "postgres"
# password = "tu_contraseña"
# GOOGLE_API_KEY = "tu_api_key"

# 3. Base de datos
createdb votape_db
python -c "from src.database import seed_data; seed_data()"

# 4. Ejecutar
streamlit run app.py
```

Disponible en `http://localhost:8501`

## � Características Técnicas

| Componente                 | Descripción                                            |
| -------------------------- | ------------------------------------------------------ |
| **app.py**                 | Dashboard con galería de candidatos                    |
| **Asistente_IA.py**        | Chat con Gemini usando RAG (solo cita datos oficiales) |
| **Comparar_Propuestas.py** | Buscador de propuestas por similitud                   |
| **Análisis**               | Sentimiento automatizado y temas prioritarios          |

## 📈 Flujos de Uso

### Ciudadano Informado

1. Abre VotoClaro
2. Ve galería de candidatos
3. Hace click en candidato para perfil detallado
4. Lee sus propuestas y temas prioritarios
5. Vuelve a comparar otros candidatos

### Usuario Comparativo

1. Va a "Comparador de Propuestas"
2. Busca tema que le preocupa (ej: "Seguridad")
3. Ve propuestas de todos los candidatos sobre ese tema
4. Identifica similitudes y diferencias
5. Toma decisiones informadas

### Usuario Curioso (Chat IA)

1. Va a "Asistente Cívico"
2. Hace preguntas específicas (ej: "¿Quién propone penas más duras?")
3. IA busca en propuestas y resume
4. Usuario profundiza con más preguntas
5. Mantiene histórico de conversación

## 📋 Roadmap

- **En Progreso**: Web scraping de JNE y ONPE
- **Próximas fases**:
  - Integración con datos reales de candidatos 2026
  - Análisis promesas vs cumplimiento
  - Exportar comparativas a PDF
  - Validación de fact-checkers integrada

**🇵🇪 VotoClaro: Democracia informada es mejor democracia**
