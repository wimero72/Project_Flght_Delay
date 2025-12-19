import pandas as pd
import joblib
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="FlightOnTime DS Model API")

# Paths
MODEL_PATH = '../models/flight_delay_model.joblib'
ENCODERS_PATH = '../models/encoders.joblib'

# Global variables for artifacts
model = None
encoders = None

class FlightInput(BaseModel):
    airline: str
    origin: str
    destination: str
    departure_date: str # ISO format
    distance: float    # Assuming km per prompt, need to check model units (likely miles)

@app.on_event("startup")
def load_artifacts():
    global model, encoders
    try:
        # Adjust paths for execution from 'datascience/api' or root
        # We will assume running from 'datascience/api' or handle relative paths carefully.
        # Let's try to find them.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_p = os.path.join(base_dir, MODEL_PATH)
        enc_p = os.path.join(base_dir, ENCODERS_PATH)
        
        print(f"Loading model from {model_p}")
        model = joblib.load(model_p)
        print(f"Loading encoders from {enc_p}")
        encoders = joblib.load(enc_p)
        print("Artifacts loaded successfully.")
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        # Dont crash, just fail requests
        pass

def preprocess(input_data: FlightInput):
    # Features: ['Airline', 'Origin', 'Destination', 'Distance', 'dep_hour', 'dep_day_of_week', 'dep_month']
    
    dt = datetime.fromisoformat(input_data.departure_date)
    dep_hour = dt.hour
    dep_day_of_week = dt.weekday()
    dep_month = dt.month
    
    # Distance conversion: KM to Miles (approx 0.621371)
    # Assuming model trained on Miles (standard for BTS/Kaggle US data)
    distance_miles = input_data.distance * 0.621371
    
    # Categorical handling
    # We need to handle unseen labels safely (e.g. put them to a default or known class if using proper encoders, 
    # but LabelEncoder fails on unseen. For MVP, we catch basic errors or try best match)
    
    # Helper to encode with fallback
    def safe_encode(col_name, value):
        le = encoders[col_name]
        try:
            return le.transform([str(value)])[0]
        except:
            # Fallback to first class or a specific 'unknown' if we had one. 
            # For MVP, just returning 0 is safe enough to prevent crash, though accuracy drops.
            print(f"Warning: Unknown category '{value}' for {col_name}")
            return 0 

    encoded_airline = safe_encode('Airline', input_data.airline)
    encoded_origin = safe_encode('Origin', input_data.origin)
    encoded_dest = safe_encode('Destination', input_data.destination)
    
    features = pd.DataFrame([{
        'Airline': encoded_airline,
        'Origin': encoded_origin,
        'Destination': encoded_dest,
        'Distance': distance_miles,
        'dep_hour': dep_hour,
        'dep_day_of_week': dep_day_of_week,
        'dep_month': dep_month
    }])
    
    return features

@app.post("/predict_model")
def predict(input_data: FlightInput):
    if not model or not encoders:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        X = preprocess(input_data)
        # Predict probability of class 1 (Delayed)
        prob = model.predict_proba(X)[0][1]
        prediction_label = "Retrasado" if prob > 0.5 else "Puntual"
        
        return {
            "prediction": prediction_label,
            "probability": float(prob)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
