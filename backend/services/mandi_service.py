import pandas as pd
import joblib
from backend.config import DATA_DIR, MODEL_DIR

mandi_df = pd.read_csv(DATA_DIR / "mandi_dataset.csv")
model = joblib.load(MODEL_DIR / "mandi_model.pkl")

def forecast_price(state, district, crop):

    df = mandi_df.copy()

    df = df[
        (df["state"].str.lower() == state.lower()) &
        (df["district"].str.lower() == district.lower()) &
        (df["crop"].str.lower() == crop.lower())
    ]

    if df.empty:
        return {"message": "No price data found"}

    latest = df.tail(1)

    predicted_price = model.predict(latest[["feature1", "feature2"]])

    return {
        "crop": crop,
        "forecast_price": float(predicted_price[0])
    }