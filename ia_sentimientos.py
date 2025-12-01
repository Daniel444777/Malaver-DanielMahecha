import pandas as pd
import psycopg2
from transformers import pipeline

# --- 1. CONFIGURACIÓN ---
# Descargamos el modelo de IA específico para opiniones multilingües (Página 41)
print("⏳ Cargando modelo de IA (esto puede tardar la primera vez)...")
analizador = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# --- 2. CONEXIÓN A BASE DE DATOS ---
try:
    conn = psycopg2.connect(
        dbname="escuela_psql",
        user="postgres",
        password="1234",  # <--- ¡TU CLAVE AQUÍ!
        host="localhost",
        port="5432"
    )
except Exception as e:
    print(f"Error de conexión: {e}")
    exit()

# --- 3. TRAER LOS COMENTARIOS ---
query = """
SELECT 
    e.nombre, 
    c.nombre AS curso, 
    m.comentario 
FROM matriculas m
JOIN estudiantes e ON m.estudiante_id = e.id
JOIN cursos c ON m.curso_codigo = c.codigo
WHERE m.comentario IS NOT NULL;
"""
df = pd.read_sql(query, conn)
conn.close()

# --- 4. ANALIZAR CADA COMENTARIO ---
print("\n--- 🧠 RESULTADOS DEL ANÁLISIS DE SENTIMIENTO ---\n")

# Recorremos cada fila de datos
for index, row in df.iterrows():
    comentario = row['comentario']
    nombre = row['nombre']
    
    # La IA lee el comentario aquí:
    resultado = analizador(comentario)[0]
    
    # El modelo devuelve estrellas (1 star = Muy malo, 5 stars = Excelente)
    estrellas = int(resultado['label'].split()[0])
    
    # Traducimos estrellas a texto para entender mejor
    if estrellas >= 4:
        sentimiento = "🟢 POSITIVO"
    elif estrellas == 3:
        sentimiento = "🟡 NEUTRAL"
    else:
        sentimiento = "🔴 NEGATIVO"

    print(f"Estudiante: {nombre}")
    print(f"Dijo: '{comentario}'")
    print(f"IA Detectó: {sentimiento} ({estrellas}/5 estrellas)")
    print("-" * 50)