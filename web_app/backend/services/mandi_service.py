import pandas as pd
import joblib
from ..config import DATA_DIR

MODEL_PATH = DATA_DIR / "mandi_price_xgboost.pkl"  # Adjust path as per project structure

try:
    model = joblib.load(MODEL_PATH)
    has_model = True
except:
    model = None
    has_model = False

mandi_df = pd.read_csv(DATA_DIR / "cleaned_mandi_prices.csv")

def forecast_price(state: str, district: str, crop: str):
    df = mandi_df[ 
        (mandi_df["state"].str.lower() == state.lower()) &
        (df["district"].str.lower() == district.lower()) &
        (df["crop"].str.lower() == crop.lower())
    ]
    
    if df.empty:
        return {"error": "No data found"}
    
    if has_model:
        features = ["feature1", "feature2"]  # Adjust to actual model features from mandi_step2_feature_engineering
        X = df[features].fillna(0)
        predicted_price = model.predict(X)[0]
    else:
        predicted_price = df["modal_price"].mean()
    
    return {
        "crop": crop,
        "current_price": float(df["modal_price"].iloc[-1]),
        "forecast_price": float(predicted_price),
        "trend": "up" if predicted_price > df["modal_price"].mean() else "down"
    }

