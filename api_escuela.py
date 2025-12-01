from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# --- 1. ENTRENAR EL MODELO AL INICIAR ---
print("⏳ Conectando a la BD y entrenando modelo...")

try:
    conn = psycopg2.connect(
        dbname="escuela_psql",
        user="postgres",
        password="1234",  # <--- ¡TU CLAVE AQUÍ!
        host="localhost",
        port="5432"
    )
    
    # Traemos los datos
    query = """
    SELECT e.edad, c.creditos, m.calificacion
    FROM estudiantes e
    JOIN matriculas m ON e.id = m.estudiante_id
    JOIN cursos c ON m.curso_codigo = c.codigo
    WHERE m.calificacion IS NOT NULL;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Entrenamos la IA (Regresión Lineal)
    X = df[['edad', 'creditos']]
    y = df['calificacion']
    modelo = LinearRegression()
    modelo.fit(X, y)
    print("✅ ¡Modelo entrenado y listo para predecir!")

except Exception as e:
    print(f"❌ Error fatal: {e}")
    exit()

# --- 2. DEFINIR LA RUTA DE LA API (Página 58) ---
@app.route('/predecir', methods=['POST'])
def predecir_nota():
    try:
        # Recibir los datos que envíe el usuario (JSON)
        datos = request.json
        
        # Extraer edad y créditos
        edad_usuario = datos['edad']
        creditos_usuario = datos['creditos']
        
        # Preguntarle al modelo
        prediccion = modelo.predict([[edad_usuario, creditos_usuario]])[0]
        
        # Devolver la respuesta
        return jsonify({
            'mensaje': 'Predicción exitosa',
            'nota_predicha': round(prediccion, 2),
            'estado': 'Aprobado' if prediccion >= 6 else 'Reprobado'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

# --- 3. ENCENDER EL SERVIDOR ---
if __name__ == '__main__':
    print("🚀 Servidor corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)