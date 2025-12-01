import pandas as pd
import psycopg2
import plotly.express as px

# 1. CONEXIÓN (La misma de siempre)
try:
    conn = psycopg2.connect(
        dbname="escuela_psql",
        user="postgres",
        password="1234",  # <--- ¡TU CLAVE AQUÍ!
        host="localhost",
        port="5432"
    )
except Exception as e:
    print(f"Error: {e}")
    exit()

# 2. CONSULTA SQL MULTIDIMENSIONAL (Basado en Página 45/57)
# Traemos nombre del estudiante, curso, nota, creditos y edad
query = """
SELECT 
    e.nombre AS estudiante,
    e.edad,
    c.nombre AS curso,
    c.creditos,
    m.calificacion
FROM estudiantes e
JOIN matriculas m ON e.id = m.estudiante_id
JOIN cursos c ON m.curso_codigo = c.codigo;
"""

df = pd.read_sql(query, conn)
conn.close()

# 3. CREAR GRÁFICO INTERACTIVO (Página 57)
print("Generando gráfico...")

fig = px.scatter(
    df, 
    x="creditos", 
    y="calificacion",
    size="edad",              # El tamaño de la burbuja depende de la edad
    color="curso",            # Diferente color para cada materia
    hover_name="estudiante",  # Al pasar el mouse, muestra el nombre
    size_max=60,
    title="Rendimiento Académico: Créditos vs Calificación",
    template="plotly_dark"    # Tema oscuro (se ve más 'pro')
)

# 4. GUARDAR Y MOSTRAR
fig.write_html("reporte_interactivo.html")
print("✅ ¡Listo! Se ha creado el archivo 'reporte_interactivo.html'.")
print("Ve a tu carpeta y ábrelo con Chrome o Edge.")