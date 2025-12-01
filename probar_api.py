import requests
import json

# Esta es la dirección de tu API
url = "http://127.0.0.1:5000/predecir"

# Datos de un estudiante nuevo que queremos evaluar
datos_estudiante = {
    "edad": 22,
    "creditos": 5
}

print(f"📡 Enviando datos a la IA: {datos_estudiante}")

try:
    # Enviamos la petición POST
    respuesta = requests.post(url, json=datos_estudiante)
    
    # Mostramos lo que respondió la IA
    print("\n--- 🤖 RESPUESTA DEL SERVIDOR ---")
    print(respuesta.text)
    
except Exception as e:
    print(f"Error: {e}")
    print("¿Asegúrate de que 'api_escuela.py' esté ejecutándose en otra terminal!")