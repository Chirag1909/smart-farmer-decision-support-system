import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
YIELD_PRED_FILE = "yield_predictions.csv"
CROP_ECON_FILE = "crop_price_cost.csv"
OUTPUT_FILE = "profit_forecast.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
print("Loading yield predictions...")
yield_df = pd.read_csv(YIELD_PRED_FILE)

print("Loading crop economics data...")
econ_df = pd.read_csv(CROP_ECON_FILE)

# -----------------------------
# MERGE DATA
# -----------------------------
df = yield_df.merge(econ_df, on="crop_type", how="left")

# -----------------------------
# PROFIT CALCULATION
# -----------------------------
df["revenue"] = df["predicted_yield"] * df["price_per_ton"]
df["profit"] = df["revenue"] - df["cost_per_hectare"]

# -----------------------------
# RANKING
# -----------------------------
df["profit_rank"] = df["profit"].rank(ascending=False)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print("Profit forecasting completed successfully.")
