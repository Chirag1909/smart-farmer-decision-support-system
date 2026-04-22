import pandas as pd
import joblib
import numpy as np
from ..config import DATA_DIR

# Load data
crop_df = pd.read_csv(DATA_DIR / "crop_model_dataset.csv")
crop_df.columns = crop_df.columns.str.lower().str.strip()

# Load model
try:
    model = joblib.load(DATA_DIR / "crop_recommendation_model.pkl")
except:
    model = joblib.load(DATA_DIR / "rf_crop_model.pkl")  # fallback

features = ["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph", "rainfall"]

def get_top_crops(state: str, district: str):
    df = crop_df.copy()
    df = df[
        (df["state"].str.lower() == state.lower()) &
        (df["district"].str.lower() == district.lower())
    ]
    if df.empty:
        return {"error": f"No data for {state}/{district}"}
    
    # Predict if features present
    if all(f in df.columns for f in features):
        df["predicted_yield"] = model.predict(df[features].fillna(0))
    else:
        df["predicted_yield"] = df.get("yield", 50.0)  # dummy fallback
    
    top5 = df.nlargest(5, "predicted_yield")[["crop", "predicted_yield"]]
    return top5.to_dict(orient="records")

