import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1. CONEXIÓN (Igual que antes)
conn = psycopg2.connect(
    dbname="escuela_psql",
    user="postgres",
    password="1234", # <--- ¡Pon tu clave aquí otra vez!
    host="localhost",
    port="5432"
)

# 2. OBTENER DATOS (Edad y Créditos)
query = "SELECT edad, creditos FROM estudiantes e JOIN matriculas m ON e.id = m.estudiante_id JOIN cursos c ON m.curso_codigo = c.codigo"
df = pd.read_sql(query, conn)
conn.close()

# 3. ENTRENAR IA (K-MEANS) - Página 23 del PDF
# Le pedimos a la IA que encuentre 3 grupos diferentes
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(df[['edad', 'creditos']])

# 4. VISUALIZAR RESULTADOS
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['edad'], df['creditos'], c=df['cluster'], cmap='viridis', s=100)
plt.xlabel('Edad')
plt.ylabel('Créditos del Curso')
plt.title('Grupos de Estudiantes (Clustering K-Means)')
plt.colorbar(scatter, label='Grupo (Cluster)')
plt.grid(True, alpha=0.3)
plt.show()

print("¡Análisis de Clustering completado! Mira el gráfico generado.")