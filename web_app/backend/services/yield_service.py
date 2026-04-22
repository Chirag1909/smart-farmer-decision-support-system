import pandas as pd
from ..config import DATA_DIR

yield_df = pd.read_csv(DATA_DIR / "yield_predictions.csv")

def get_yield_predictions(state: str):
    df = yield_df[yield_df["state"].str.lower() == state.lower()]
    if df.empty:
        return {"error": "No yield data"}
    return df[["crop", "predicted_yield", "district"]].head(10).to_dict(orient="records")

