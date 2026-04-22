import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "processed_data", "yield_features.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "processed_data", "yield_predictions.csv")

TARGET = "yield"


def extract_crop(row, crop_columns):
    for col in crop_columns:
        if row[col] is True or row[col] == 1:
            return col.replace("crop_", "")
    return "unknown"


def train_and_predict():

    print("Loading yield features...")
    df = pd.read_csv(INPUT_FILE)

    # Identify crop one-hot columns
    crop_columns = [c for c in df.columns if c.startswith("crop_")]

    if not crop_columns:
        raise ValueError("No crop one-hot columns found in dataset")

    # Reconstruct crop name
    df["crop_name"] = df.apply(lambda r: extract_crop(r, crop_columns), axis=1)

    # Feature matrix and target
    X = df.drop(columns=[TARGET, "crop_name"])
    y = df[TARGET]

    # ✅ FIXED unpacking
    X_train, X_test, y_train, y_test, crop_train, crop_test = train_test_split(
        X,
        y,
        df["crop_name"],
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    print("Training yield prediction model...")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    print(f"Yield Model MAE: {mae:.2f}")

    # Output for profit forecasting
    output = pd.DataFrame({
        "crop": crop_test.values,
        "predicted_yield": preds
    })

    output.to_csv(OUTPUT_FILE, index=False)
    print("Yield predictions saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    train_and_predict()
