import pandas as pd
import numpy as np

ranking_df = pd.read_csv("processed_data/best_crop_mandi_ranking.csv")
mandi_df = pd.read_csv("processed_data/mandi_prices.csv")

def get_states():
    return sorted(ranking_df["state"].unique())

def top_k_crops(state):
    df = ranking_df[ranking_df["state"] == state]
    return df.sort_values(by="predicted_yield", ascending=False).head(5)

def profit_forecast(state):
    df = ranking_df[ranking_df["state"] == state]
    df["profit"] = df["predicted_yield"] * df["modal_price"]
    return df.sort_values(by="profit", ascending=False).head(5)

def mandi_prices(state):
    df = mandi_df[mandi_df["state"] == state]
    return df.head(10)

def forecast_price(state, crop):
    df = mandi_df[
        (mandi_df["state"] == state) &
        (mandi_df["commodity"] == crop)
    ]

    prices = df["modal_price"].values[-5:]
    forecast = []

    for i in range(5):
        pred = np.mean(prices[-3:])
        forecast.append(round(pred, 2))
        prices = np.append(prices, pred)

    return forecast