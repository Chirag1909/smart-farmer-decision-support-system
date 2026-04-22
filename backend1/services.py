import pandas as pd
from backend.config import YIELD_FILE, STEP5_FILE, STEP6_FILE


def load_yield_data():
    return pd.read_csv(YIELD_FILE)


def load_step5_data():
    return pd.read_csv(STEP5_FILE)


def load_step6_data():
    return pd.read_csv(STEP6_FILE)


def get_top_yield_crops(n=5):
    df = load_yield_data()
    return df.sort_values("predicted_yield", ascending=False).head(n)


def get_best_profit_crops(n=5):
    df = load_step6_data()
    return df.sort_values("net_profit", ascending=False).head(n)
