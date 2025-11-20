-- Tabla de Candidatos
CREATE TABLE IF NOT EXISTS candidatos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    partido VARCHAR(255) NOT NULL,
    foto_url TEXT,
    biografia_resumen TEXT
);

-- Tabla de Propuestas / Discurso (Texto crudo + Embeddings futuros)
CREATE TABLE IF NOT EXISTS propuestas (
    id SERIAL PRIMARY KEY,
    candidato_id INTEGER REFERENCES candidatos(id),
    tema VARCHAR(100), -- Ej: Economía, Salud
    contenido TEXT NOT NULL, -- El fragmento de texto o propuesta
    fuente_url TEXT, -- Link a Youtube o JNE para transparencia
    fecha_registro DATE DEFAULT CURRENT_DATE
);

-- Tabla de Métricas de IA (Para los gráficos rápidos)
CREATE TABLE IF NOT EXISTS metricas (
    id SERIAL PRIMARY KEY,
    candidato_id INTEGER REFERENCES candidatos(id),
    tipo_metrica VARCHAR(50), -- Ej: 'sentimiento_promedio', 'coherencia'
    valor FLOAT, -- Ej: 0.75 (positivo), 0.2 (negativo)
    detalle_json JSONB -- Para guardar data extra si hace falta
);