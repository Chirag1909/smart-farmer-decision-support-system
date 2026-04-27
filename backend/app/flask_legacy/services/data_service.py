import os
from functools import lru_cache

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "processed_data")

RANKING_PATH = os.path.join(PROCESSED_DIR, "best_crop_mandi_ranking.csv")
MANDI_PATH = os.path.join(PROCESSED_DIR, "cleaned_mandi_prices.csv")
COST_PATH = os.path.join(PROCESSED_DIR, "best_crop_net_profit_ranking.csv")


def _normalize_crop(crop_name: str) -> str:
    return str(crop_name).replace("type_", "").strip()


@lru_cache(maxsize=1)
def load_data():
    ranking_df = pd.read_csv(RANKING_PATH)
    mandi_df = pd.read_csv(MANDI_PATH)
    cost_df = pd.read_csv(COST_PATH)

    ranking_df["crop"] = ranking_df["crop"].map(_normalize_crop)
    mandi_df["crop"] = mandi_df["crop"].map(_normalize_crop)
    cost_df["crop"] = cost_df["crop"].map(_normalize_crop)

    ranking_df["state_key"] = ranking_df["state"].str.lower().str.strip()
    mandi_df["state_key"] = mandi_df["state"].str.lower().str.strip()
    cost_df["cost_per_hectare"] = pd.to_numeric(cost_df["cost_per_hectare"], errors="coerce")
    ranking_df["predicted_yield"] = pd.to_numeric(ranking_df["predicted_yield"], errors="coerce")
    ranking_df["modal_price"] = pd.to_numeric(ranking_df["modal_price"], errors="coerce")
    mandi_df["modal_price"] = pd.to_numeric(mandi_df["modal_price"], errors="coerce")

    crop_cost = (
        cost_df.groupby("crop", as_index=False)["cost_per_hectare"].median().rename(
            columns={"cost_per_hectare": "estimated_cost_per_hectare"}
        )
    )
    return ranking_df, mandi_df, crop_cost


def get_states():
    ranking_df, _, _ = load_data()
    return sorted(ranking_df["state"].dropna().unique().tolist())


def get_recommendations(state: str, top_k: int = 5):
    ranking_df, _, crop_cost = load_data()
    state_key = state.lower().strip()
    subset = ranking_df[ranking_df["state_key"] == state_key].copy()
    if subset.empty:
        return []

    agg = (
        subset.groupby(["state", "crop"], as_index=False)[["predicted_yield", "modal_price"]]
        .median()
        .sort_values("predicted_yield", ascending=False)
    )
    agg = agg.merge(crop_cost, on="crop", how="left")
    agg["estimated_cost_per_hectare"] = agg["estimated_cost_per_hectare"].fillna(
        agg["estimated_cost_per_hectare"].median()
    ).fillna(50000.0)
    return agg.head(top_k).to_dict(orient="records")


def get_profit_analysis(state: str, top_k: int = 5):
    _, mandi_df, _ = load_data()
    recommendations = get_recommendations(state, top_k=25)
    if not recommendations:
        return []

    rec_df = pd.DataFrame(recommendations)
    state_key = state.lower().strip()
    mandi_state = mandi_df[mandi_df["state_key"] == state_key].copy()

    best_mandi = (
        mandi_state.sort_values("modal_price", ascending=False)[["crop", "market", "modal_price"]]
        .drop_duplicates(subset=["crop"])
        .rename(columns={"modal_price": "best_market_price"})
    )

    merged = rec_df.merge(best_mandi, on="crop", how="left")
    merged["effective_price"] = merged["best_market_price"].fillna(merged["modal_price"])
    merged["expected_revenue"] = merged["predicted_yield"] * merged["effective_price"]
    merged["expected_profit"] = merged["expected_revenue"] - merged["estimated_cost_per_hectare"]
    merged["profit_margin"] = (
        merged["expected_profit"] / merged["expected_revenue"].replace(0, pd.NA)
    ).fillna(0.0) * 100
    merged = merged.sort_values("expected_profit", ascending=False)
    return merged.head(top_k).to_dict(orient="records")


def get_mandi_comparison(state: str, crop: str = "", limit: int = 20):
    _, mandi_df, _ = load_data()
    state_key = state.lower().strip()
    subset = mandi_df[mandi_df["state_key"] == state_key].copy()
    if crop:
        crop_key = crop.lower().strip()
        subset = subset[subset["crop"].str.lower() == crop_key]
    if subset.empty:
        return []
    subset = subset.sort_values("modal_price", ascending=False).head(limit)
    return subset[
        ["state", "district", "market", "crop", "modal_price", "date"]
    ].to_dict(orient="records")
