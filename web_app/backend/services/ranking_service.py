import pandas as pd
from ..config import DATA_DIR

ranking_df = pd.read_csv(DATA_DIR / "best_crop_mandi_ranking.csv")

def get_crop_ranking(state: str):
    df = ranking_df[ranking_df["state"].str.lower() == state.lower()]
    if df.empty:
        return {"error": "No ranking data"}
    top5 = df.head(5)[["crop", "expected_revenue"]]
    return top5.to_dict(orient="records")

