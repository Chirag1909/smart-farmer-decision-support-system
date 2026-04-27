from fastapi import APIRouter
import pandas as pd

router = APIRouter(
    prefix="/profit",
    tags=["Profit"]
)

@router.get("/state/{state}")
def get_profit(state: str):
    df = pd.read_csv("processed_data/best_crop_mandi_ranking.csv")
    df = df[df["state"].str.lower() == state.lower()]
    df = df.sort_values("expected_revenue", ascending=False).head(5)

    return df.to_dict(orient="records")