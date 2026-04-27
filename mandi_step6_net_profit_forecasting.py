import pandas as pd
import os

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "processed_data", "best_crop_mandi_ranking.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "processed_data", "best_crop_net_profit_ranking.csv")

# ---------------- LOAD DATA ----------------
print("Loading Step-5 ranking data...")
df = pd.read_csv(INPUT_FILE)

df.columns = df.columns.str.lower().str.strip()

# ---------------- CLEAN CROP NAME ----------------
df["crop_clean"] = (
    df["crop"]
    .str.replace("type_", "", regex=False)
    .str.lower()
    .str.strip()
)

# ---------------- ESTIMATED COST TABLE ----------------
# (Academic assumption – acceptable for project)
estimated_cost = {
    "rice": 35000,
    "wheat": 30000,
    "maize": 28000,
    "cotton": 42000,
    "sugarcane": 50000,
    "coffee": 60000,
    "rubber": 55000,
    "coconut": 45000,
    "black pepper": 70000,
    "ginger": 65000,
}

df["cost_per_hectare"] = df["crop_clean"].map(estimated_cost)

# ---------------- HANDLE UNKNOWN CROPS ----------------
df["cost_per_hectare"] = df["cost_per_hectare"].fillna(
    df["cost_per_hectare"].median()
)

# ---------------- NET PROFIT ----------------
df["net_profit"] = df["expected_revenue"] - df["cost_per_hectare"]

# ---------------- FINAL RANKING ----------------
df = df.sort_values("net_profit", ascending=False)
df["profit_rank"] = range(1, len(df) + 1)

# ---------------- SAVE ----------------
final_cols = [
    "profit_rank",
    "crop",
    "predicted_yield",
    "modal_price",
    "expected_revenue",
    "cost_per_hectare",
    "net_profit"
]

df[final_cols].to_csv(OUTPUT_FILE, index=False)

# ---------------- OUTPUT ----------------
print(" Step-6 Net Profit Forecasting Completed")
print(f"Saved to: {OUTPUT_FILE}")
print("\nTop 5 Net Profit Crops:")
print(df[final_cols].head())
