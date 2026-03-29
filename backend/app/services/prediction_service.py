import pickle
import pandas as pd
from app.models.db_models import Prediction

# Load model
with open("app/models/model.pkl", "rb") as f:
    model = pickle.load(f)

# 🔥 DEFAULT TEMPLATE (IMPORTANT)
# These must match your training dataset columns
DEFAULT_INPUT = {
    "distance_km": 0,
    "driver_rating": 0,
    "holiday_flag": 0,
    "day_of_week": 0,
    "destination_city": "Unknown"
}

def predict_and_save(data: dict, db):
    # 🔥 Step 1: Merge user input with default
    full_data = DEFAULT_INPUT.copy()
    full_data.update(data)

    df = pd.DataFrame([full_data])

    # 🔥 Step 2: Apply same preprocessing
    df = pd.get_dummies(df)

    # 🔥 Step 3: Fix missing columns manually
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0

    # Ensure correct column order
    df = df[model.feature_names_in_]

    # Prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    # Save to DB
    record = Prediction(
        distance=data.get("distance", 0),
        carrier=data.get("carrier", "Unknown"),
        weather=data.get("weather", "Unknown"),
        prediction=int(prediction),
        probability=float(probability)
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }