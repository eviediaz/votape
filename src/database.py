# src/database.py
import streamlit as st
import sqlalchemy
from sqlalchemy import text

def get_db_engine():
    """Crea y devuelve el motor de conexión a la base de datos usando st.secrets"""
    try:
        db_config = st.secrets["connections"]["postgresql"]
        # Construimos la URL de conexión
        db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        engine = sqlalchemy.create_engine(db_url)
        return engine
    except Exception as e:
        st.error(f"Error configurando la DB: {e}")
        return None

def seed_data():
    """Borra los datos existentes e inserta datos de prueba para el MVP"""
    engine = get_db_engine()
    if engine is None:
        return

    with engine.connect() as conn:
        trans = conn.begin() # Iniciar transacción
        try:
            # 1. Limpiar tablas (TRUNCATE para reiniciar IDs)
            st.info("🧹 Limpiando base de datos...")
            conn.execute(text("TRUNCATE metricas, propuestas, candidatos RESTART IDENTITY CASCADE;"))
            
            # 2. Insertar Candidatos (Ejemplos arquetípicos Perú 2026)
            st.info("👤 Insertando candidatos...")
            conn.execute(text("""
                INSERT INTO candidatos (nombre, partido, foto_url, biografia_resumen) VALUES
                ('Keiko Fujimori', 'Fuerza Popular', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Keiko_Fujimori_in_2016_%28cropped%29.jpg/220px-Keiko_Fujimori_in_2016_%28cropped%29.jpg', 'Lideresa de Fuerza Popular. Ex congresista. Ha postulado a la presidencia en múltiples ocasiones.'),
                ('Antauro Humala', 'A.N.T.A.U.R.O', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Antauro_Humala_%28cropped%29.jpg/220px-Antauro_Humala_%28cropped%29.jpg', 'Líder etnocacerista. Recientemente liberado y con discurso radical sobre reformas constitucionales.'),
                ('Carlos Añaños', 'Perú Moderno', 'https://portal.andina.pe/EDPfotografia3/Thumbnail/2020/09/23/000708167W.jpg', 'Empresario ayacuchano fundador del Grupo AJE. Enfoque en economía y emprendimiento.')
            """))

            # 3. Insertar Métricas Simuladas (Para los gráficos)
            st.info("📊 Insertando métricas de IA simuladas...")
            # Keiko: Sentimiento mixto, Temas: Economía y Seguridad
            conn.execute(text("""
                INSERT INTO metricas (candidato_id, tipo_metrica, valor, detalle_json) VALUES
                (1, 'sentimiento_promedio', 0.45, '{"positivo": 30, "neutro": 40, "negativo": 30}'),
                (1, 'tema_prioritario', 0.60, '{"tema": "Seguridad", "peso": 0.6}'),
                (1, 'tema_prioritario', 0.30, '{"tema": "Economía", "peso": 0.3}')
            """))
            # Antauro: Sentimiento negativo (crítico), Temas: Constitución y Justicia
            conn.execute(text("""
                INSERT INTO metricas (candidato_id, tipo_metrica, valor, detalle_json) VALUES
                (2, 'sentimiento_promedio', 0.30, '{"positivo": 20, "neutro": 20, "negativo": 60}'),
                (2, 'tema_prioritario', 0.70, '{"tema": "Constitución", "peso": 0.7}'),
                (2, 'tema_prioritario', 0.20, '{"tema": "Corrupción", "peso": 0.2}')
            """))
            # Añaños: Sentimiento positivo, Temas: Empleo e Innovación
            conn.execute(text("""
                INSERT INTO metricas (candidato_id, tipo_metrica, valor, detalle_json) VALUES
                (3, 'sentimiento_promedio', 0.75, '{"positivo": 60, "neutro": 30, "negativo": 10}'),
                (3, 'tema_prioritario', 0.50, '{"tema": "Economía", "peso": 0.5}'),
                (3, 'tema_prioritario', 0.40, '{"tema": "Agricultura", "peso": 0.4}')
            """))

            # 4. Insertar Propuestas (Para el buscador de similitud futuro)
            st.info("📜 Insertando propuestas de prueba...")
            conn.execute(text("""
                INSERT INTO propuestas (candidato_id, tema, contenido, fuente_url) VALUES
                (1, 'Seguridad', 'Construiremos nuevas cárceles a 4000 msnm para aislar a criminales peligrosos.', 'https://youtube.com/link_keiko'),
                (2, 'Constitución', 'Aplicaremos la pena capital para casos de corrupción macro en el estado.', 'https://youtube.com/link_antauro'),
                (3, 'Economía', 'Impulsaremos créditos baratos para las PYMES y reducción de trabas burocráticas.', 'https://youtube.com/link_ananos')
            """))

            trans.commit() # Guardar cambios
            st.success("✅ ¡Datos de prueba cargados exitosamente!")
            
        except Exception as e:
            trans.rollback()
            st.error(f"❌ Error insertando datos: {e}")