import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# --- PASO 1: CONEXIÓN A SQL (Página 21) ---
try:
    conn = psycopg2.connect(
        dbname="escuela_psql",
        user="postgres",
        password="1234",  # <--- ¡CAMBIA ESTO POR TU CONTRASEÑA!
        host="localhost",
        port="5432"
    )
    print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit()

# --- PASO 2: EXTRAER DATOS PARA IA (Página 19/21) ---
# Usamos la consulta que ya probaste en tu captura de pantalla
query = """
SELECT 
    e.edad, 
    c.creditos, 
    m.calificacion
FROM estudiantes e
JOIN matriculas m ON e.id = m.estudiante_id
JOIN cursos c ON m.curso_codigo = c.codigo
WHERE m.calificacion IS NOT NULL;
"""

df = pd.read_sql(query, conn)
conn.close() # Cerramos la conexión, ya tenemos los datos en pandas

print("\n--- Vista previa de los datos ---")
print(df.head())

# --- PASO 3: ENTRENAR EL MODELO (Página 22) ---
# Queremos predecir la 'calificacion' basándonos en 'edad' y 'creditos'

# X = Variables predictoras (Edad, Créditos)
X = df[['edad', 'creditos']] 
# y = Variable objetivo (Calificación)
y = df['calificacion']

# Dividir datos: 80% para entrenar, 20% para probar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de Regresión Lineal
modelo = LinearRegression()

# Entrenar el modelo (aquí es donde la IA "aprende")
modelo.fit(X_train, y_train)

# --- PASO 4: EVALUAR RESULTADOS ---
predicciones = modelo.predict(X_test)
error = mean_squared_error(y_test, predicciones)

print(f"\nError Cuadrático Medio (MSE): {error:.2f}")
print("Predicciones vs Realidad:")
for pred, real in zip(predicciones, y_test):
    print(f"Predicho: {pred:.2f} | Real: {real}")

# (Opcional) Gráfico simple
plt.scatter(y_test, predicciones)
plt.xlabel('Valores Reales')
plt.ylabel('Predicciones')
plt.title('Regresión Lineal: Calificaciones')
plt.show()