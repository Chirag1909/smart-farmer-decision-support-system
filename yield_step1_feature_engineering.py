# yield_step1_feature_engineering.py

import pandas as pd
import os

INPUT_FILE = "Crop Yield Prediction/yield_prediction_dataset.csv"
OUTPUT_FILE = "processed_data/yield_features.csv"

def assign_season(month):
    if month in [6, 7, 8, 9]:
        return "Kharif"
    elif month in [10, 11, 12, 1]:
        return "Rabi"
    else:
        return "Zaid"

def feature_engineering(input_file, output_file):
    print("Loading yield dataset...")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Dataset not found at: {input_file}")

    df = pd.read_csv(input_file)
    print("Initial shape:", df.shape)

    # Convert date
    df["date_of_image"] = pd.to_datetime(df["date_of_image"], errors="coerce")

    # Time features
    df["month"] = df["date_of_image"].dt.month
    df["season"] = df["month"].apply(assign_season)

    # Encode categorical variables
    df = pd.get_dummies(df, columns=["crop_type", "season"], drop_first=True)

    # Drop non-predictive columns
    df.drop(columns=["field_id", "date_of_image"], inplace=True, errors="ignore")

    # Handle missing values
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Save
    os.makedirs("processed_data", exist_ok=True)
    df.to_csv(output_file, index=False)

    print("Feature engineering completed.")
    print("Final shape:", df.shape)
    print("Saved to:", output_file)

if __name__ == "__main__":
    feature_engineering(INPUT_FILE, OUTPUT_FILE)
