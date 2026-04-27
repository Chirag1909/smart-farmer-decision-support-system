import pandas as pd
import joblib
from config import DATA_DIR, MODEL_DIR

def _load_mandi_df():
    path = DATA_DIR / "mandi_dataset.csv"
    if not path.exists():
        fallback = DATA_DIR / "processed_data_cleaned_mandi_prices.csv"
        path = fallback if fallback.exists() else path
    if not path.exists():
        return None
    return pd.read_csv(path)


def _load_model():
    path = MODEL_DIR / "mandi_model.pkl"
    if not path.exists():
        return None
    return joblib.load(path)

def forecast_price(state, district, crop):
    mandi_df = _load_mandi_df()
    model = _load_model()
    if mandi_df is None:
        return {"message": "No mandi dataset found in configured data directory"}

    df = mandi_df.copy()

    df = df[
        (df["state"].str.lower() == state.lower()) &
        (df["district"].str.lower() == district.lower()) &
        (df["crop"].str.lower() == crop.lower())
    ]

    if df.empty:
        return {"message": "No price data found"}

    if model is None:
        latest_price = df["modal_price"].dropna().iloc[-1] if "modal_price" in df.columns and not df["modal_price"].dropna().empty else 0
        return {"crop": crop, "forecast_price": float(latest_price), "source": "fallback_latest_price"}

    latest = df.tail(1)
    feature_cols = [c for c in ["feature1", "feature2"] if c in latest.columns]
    if len(feature_cols) < 2:
        latest_price = df["modal_price"].dropna().iloc[-1] if "modal_price" in df.columns and not df["modal_price"].dropna().empty else 0
        return {"crop": crop, "forecast_price": float(latest_price), "source": "fallback_latest_price"}

    predicted_price = model.predict(latest[feature_cols])

    return {
        "crop": crop,
        "forecast_price": float(predicted_price[0])
    }