import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Configuration
DATA_PATH_PRIMARY = 'data/flight_delays.csv'
DATA_PATH_FALLBACK = 'flight_delays.csv'
MODEL_DIR = 'models/'
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    if os.path.exists(DATA_PATH_PRIMARY):
        print(f"Loading data from {DATA_PATH_PRIMARY}")
        return pd.read_csv(DATA_PATH_PRIMARY)
    elif os.path.exists(DATA_PATH_FALLBACK):
        print(f"Loading data from {DATA_PATH_FALLBACK}")
        return pd.read_csv(DATA_PATH_FALLBACK)
    else:
        raise FileNotFoundError("Could not find flight_delays.csv")

def preprocess_data(df):
    print("Preprocessing data...")
    # 1. Target Variable: Delayed if DelayMinutes > 15
    df['is_delayed'] = (df['DelayMinutes'] > 15).astype(int)
    
    # 2. Datetime Features
    df['ScheduledDeparture'] = pd.to_datetime(df['ScheduledDeparture'])
    df['dep_hour'] = df['ScheduledDeparture'].dt.hour
    df['dep_day_of_week'] = df['ScheduledDeparture'].dt.dayofweek
    df['dep_month'] = df['ScheduledDeparture'].dt.month
    
    # 3. Select Features
    features = ['Airline', 'Origin', 'Destination', 'Distance', 'dep_hour', 'dep_day_of_week', 'dep_month']
    X = df[features].copy()
    y = df['is_delayed']
    
    # 4. Encode Categoricals
    encoders = {}
    cat_cols = ['Airline', 'Origin', 'Destination']
    for col in cat_cols:
        le = LabelEncoder()
        # Handle unknown categories in future by fitting on all known data now
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
        
    return X, y, encoders

def train_model(X, y):
    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print("Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    return model

def save_artifacts(model, encoders):
    print(f"Saving artifacts to {MODEL_DIR}")
    joblib.dump(model, os.path.join(MODEL_DIR, 'flight_delay_model.joblib'))
    joblib.dump(encoders, os.path.join(MODEL_DIR, 'encoders.joblib'))
    print("Save complete.")

if __name__ == "__main__":
    try:
        df = load_data()
        X, y, encoders = preprocess_data(df)
        model = train_model(X, y)
        save_artifacts(model, encoders)
    except Exception as e:
        print(f"Error: {e}")
