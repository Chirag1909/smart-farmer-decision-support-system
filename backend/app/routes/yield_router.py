from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/yield", tags=["Yield"])

@router.get("/all")
def get_all_yield():
    df = pd.read_csv("processed_data/yield_predictions.csv")
    return df.to_dict(orient="records")

@router.get("/state/{state}")
def get_yield_by_state(state: str):
    df = pd.read_csv("processed_data/yield_predictions.csv")
    df = df[df["state"].str.lower() == state.lower()]
    return df.to_dict(orient="records")
