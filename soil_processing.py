import os
import pandas as pd
from utils import standardize_columns, fill_numeric_na

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOIL_DIR = os.path.join(
    BASE_DIR,
    "Soil Nutrient Dataset of Southern Indian States"
)

# 🔍 Auto-detect CSV file
csv_files = [f for f in os.listdir(SOIL_DIR) if f.endswith(".csv")]

if not csv_files:
    raise FileNotFoundError("No CSV file found in Soil Nutrient Dataset folder")

SOIL_PATH = os.path.join(SOIL_DIR, csv_files[0])

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "soil_cleaned.csv"
)

df = pd.read_csv(SOIL_PATH)
print(f"Soil dataset loaded: {csv_files[0]}")

df = standardize_columns(df)

# Normalize column names
COLUMN_MAP = {
    "nitrogen_content": "nitrogen",
    "n": "nitrogen",
    "phosphorus_content": "phosphorus",
    "p": "phosphorus",
    "potassium_content": "potassium",
    "k": "potassium",
    "soil_ph": "ph",
    "ph_value": "ph"
}

for old, new in COLUMN_MAP.items():
    if old in df.columns:
        df.rename(columns={old: new}, inplace=True)

df = fill_numeric_na(df)

required = ["nitrogen", "phosphorus", "potassium", "ph"]
missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(f"Missing columns in soil data: {missing}")

df.to_csv(OUTPUT_PATH, index=False)
print("soil_cleaned.csv saved successfully")
