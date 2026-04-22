import pandas as pd
from ..config import DATA_DIR

profit_df = pd.read_csv(DATA_DIR / "profit_forecast.csv")

def get_profit_forecast(state: str):
    df = profit_df[profit_df["state"].str.lower() == state.lower()]
    if df.empty:
        return {"error": "No data"}
    top_crops = df.nlargest(5, "expected_profit")[["crop", "expected_profit"]]
    return top_crops.to_dict(orient="records")

