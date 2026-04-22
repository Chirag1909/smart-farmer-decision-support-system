from fastapi import FastAPI
from backend.services import (
    get_top_yield_crops,
    get_best_profit_crops
)

app = FastAPI(
    title="Hydrology Crop Decision Support API",
    version="1.0"
)

@app.get("/")
def home():
    return {"status": "API running successfully"}

# 🔹 Yield Prediction API
@app.get("/yield/top")
def top_yield_crops(limit: int = 5):
    df = get_top_yield_crops(limit)
    return df.to_dict(orient="records")

# 🔹 Best Profit API (MAIN Android API)
@app.get("/profit/best")
def best_profit_crops(limit: int = 5):
    df = get_best_profit_crops(limit)
    return df.to_dict(orient="records")
