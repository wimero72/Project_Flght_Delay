# FlightOnTime - Predictor de Retrasos de Vuelos

## Descripción
Solución MVP para predecir si un vuelo se retrasará basándose en datos históricos.
Consta de dos componentes:
1.  **Data Science Microservice (Python/FastAPI)**: Carga el modelo predictivo y expone inferencia.
2.  **Back-End API (Java/Spring Boot)**: API REST principal que valida y consulta el modelo.
## Activar entorno virtual
-   source .venv/Scripts/activate 
## Estructura del Proyecto
-   `/datascience`: Notebooks, scripts de entrenamiento, API Python y datos.
-   `/backend`: Proyecto Java Spring Boot.

## Requisitos
-   Java 17+
-   Maven 3.8+
-   Python 3.8+
-   Librerías Python: `pandas`, `scikit-learn`, `fastapi`, `uvicorn`, `joblib`

## Ejecución

### 1. Data Science (Modelo y API)
Primero, asegurar que el modelo está entrenado y la API corriendo.

```bash
# Instalar dependencias
cd datascience
pip install -r requirements.txt

# Entrenar modelo (si no existe en datasets/models)
# Asegurarse de que flight_delays.csv está en datascience/data/
python notebooks/train_model.py

# Iniciar API Python (puerto 8000)
cd api
uvicorn main:app --reload
```

### 2. Back-End (Spring Boot)
En otra terminal, iniciar la aplicación Java.

```bash
cd backend
mvn spring-boot:run
```
La aplicación correrá en `http://localhost:8080`.

## Uso del Endpoint
**Endpoint:** `POST /predict`

**Ejemplo de Request (JSON):**
```json
{
  "aerolinea": "United",
  "origen": "JFK",
  "destino": "SFO",
  "fecha_partida": "2025-11-10T14:30:00",
  "distancia_km": 350
}
```

**Ejemplo de Respuesta (JSON):**
```json
{
  "prevision": "Retrasado",
  "probabilidad": 0.78
}
```

## Dataset
Se utilizó el dataset `flight_delays.csv` (Muestra de Kaggle/Custom) que contiene histórico de vuelos y sus retrasos.
