import os
import pandas as pd
from utils import standardize_columns, fill_numeric_na

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "crops-npk data set",
    "sensor_Crop_Dataset (1).csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "crop_model_dataset.csv"
)

df = pd.read_csv(DATA_PATH)
print("Crop dataset loaded")

df = standardize_columns(df)

# Rename columns to ML-friendly names
RENAME_MAP = {
    "nitrogen": "nitrogen",
    "phosphorus": "phosphorus",
    "potassium": "potassium",
    "temperature": "temperature",
    "humidity": "humidity",
    "ph_value": "ph",
    "rainfall": "rainfall",
    "crop": "crop",
    "soil_type": "soil_type",
    "variety": "variety"
}

df.rename(columns=RENAME_MAP, inplace=True)

# Drop variety to avoid data leakage
if "variety" in df.columns:
    df.drop(columns=["variety"], inplace=True)
    print("Dropped 'variety' column")

df = fill_numeric_na(df)

required = [
    "nitrogen",
    "phosphorus",
    "potassium",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
    "crop",
    "soil_type"
]

missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns in crop data: {missing}")

df.to_csv(OUTPUT_PATH, index=False)
print("crop_model_dataset.csv saved successfully")
