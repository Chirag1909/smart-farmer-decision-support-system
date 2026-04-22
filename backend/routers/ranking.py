from fastapi import APIRouter
import pandas as pd
from pathlib import Path
import joblib

router = APIRouter(prefix="/ranking", tags=["Ranking"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load ML model
MODEL_PATH = BASE_DIR / "models" / "yield_model.pkl"
model = joblib.load(MODEL_PATH)

# Load datasets once (performance optimization)
CROP_DATA_PATH = BASE_DIR / "processed_data" / "crop_model_dataset.csv"
PRICE_DATA_PATH = BASE_DIR / "processed_data" / "cleaned_mandi_prices.csv"

crop_master_df = pd.read_csv(CROP_DATA_PATH)
price_master_df = pd.read_csv(PRICE_DATA_PATH)

# Normalize column names
crop_master_df.columns = crop_master_df.columns.str.lower().str.strip()
price_master_df.columns = price_master_df.columns.str.lower().str.strip()


@router.get("/state/{state}")
def get_ranking(state: str):

    crop_df = crop_master_df.copy()
    price_df = price_master_df.copy()

    state = state.lower().strip()

    # Filter only mandi dataset by state
    price_df["state"] = price_df["state"].str.lower().str.strip()
    price_df = price_df[price_df["state"] == state]

    if price_df.empty:
        return {"message": f"No mandi data found for {state}"}

    # Required ML features
    features = ["nitrogen", "phosphorus", "potassium", "rainfall", "temperature", "ph"]

    # Predict yield
    crop_df["predicted_yield"] = model.predict(crop_df[features])

    # Merge predicted yield with mandi price
    df = pd.merge(crop_df, price_df, on="crop")

    if df.empty:
        return {"message": "No matching crops between ML dataset and mandi dataset"}

    # Calculate revenue
    df["expected_revenue"] = df["predicted_yield"] * df["modal_price"]

    # Group by crop and take mean revenue
    df_grouped = df.groupby("crop", as_index=False).mean(numeric_only=True)

    top5 = df_grouped.sort_values("expected_revenue", ascending=False).head(5)

    return top5[["crop", "expected_revenue"]].to_dict(orient="records")