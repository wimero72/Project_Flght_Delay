import requests

# Configuración
API_URL = "http://localhost:8080/predict"

def obtener_prediccion(aerolinea, origen, destino, fecha, distancia=1000.0):
    """
    Envía los datos al backend Java y retorna la respuesta limpia.
    """
    payload = {
        "aerolinea": aerolinea,
        "origen": origen,
        "destino": destino,
        "fecha_partida": str(fecha),
        "distancia_km": distancia
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            return response.json() # Retorna el diccionario con la respuesta
        else:
            return {"error": f"Error del servidor: {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "No se pudo conectar con el servidor Java backend."}
    except Exception as e:
        return {"error": f"Ocurrió un error inesperado: {str(e)}"}