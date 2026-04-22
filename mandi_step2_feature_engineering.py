import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder


def feature_engineering(input_file, output_file):
    print("Loading cleaned mandi data...")

    df = pd.read_csv(input_file)
    print(f"Input shape: {df.shape}")

    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop invalid dates
    df.dropna(subset=["date"], inplace=True)

    # -------------------------
    # TIME FEATURES (SAFE)
    # -------------------------
    df["year"] = df["date"].dt.year.astype("int16")
    df["month"] = df["date"].dt.month.astype("int8")
    df["day"] = df["date"].dt.day.astype("int8")
    df["day_of_week"] = df["date"].dt.dayofweek.astype("int8")
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype("int8")

    # ISO week (handle NA safely)
    df["week"] = df["date"].dt.isocalendar().week
    df = df[df["week"].notna()]
    df["week"] = df["week"].astype("int16")

    # -------------------------
    # SORT FOR TIME SERIES
    # -------------------------
    df = df.sort_values(
        by=["state", "district", "market", "crop", "date"]
    )

    # -------------------------
    # LAG FEATURES
    # -------------------------
    group_cols = ["state", "district", "market", "crop"]

    df["price_lag_1"] = df.groupby(group_cols)["modal_price"].shift(1)
    df["price_lag_7"] = df.groupby(group_cols)["modal_price"].shift(7)
    df["price_lag_14"] = df.groupby(group_cols)["modal_price"].shift(14)

    # -------------------------
    # ROLLING FEATURES
    # -------------------------
    df["rolling_mean_7"] = (
        df.groupby(group_cols)["modal_price"]
        .transform(lambda x: x.rolling(7).mean())
    )

    df["rolling_mean_14"] = (
        df.groupby(group_cols)["modal_price"]
        .transform(lambda x: x.rolling(14).mean())
    )

    # Drop rows created by lag/rolling
    df.dropna(inplace=True)

    # -------------------------
    # LABEL ENCODING
    # -------------------------
    encoders = {}

    for col in group_cols:
        le = LabelEncoder()
        df[col + "_id"] = le.fit_transform(df[col])
        encoders[col] = le

    # -------------------------
    # FINAL DATASET
    # -------------------------
    feature_columns = [
        "state_id", "district_id", "market_id", "crop_id",
        "year", "month", "week", "day",
        "day_of_week", "is_weekend",
        "price_lag_1", "price_lag_7", "price_lag_14",
        "rolling_mean_7", "rolling_mean_14"
    ]

    target_column = "modal_price"

    final_df = df[feature_columns + [target_column]]

    print(f"Final ML dataset shape: {final_df.shape}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_df.to_csv(output_file, index=False)

    print(f"Feature engineered data saved to: {output_file}")


if __name__ == "__main__":

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    INPUT_FILE = os.path.join(
        PROJECT_ROOT,
        "processed_data",
        "cleaned_mandi_prices.csv"
    )

    OUTPUT_FILE = os.path.join(
        PROJECT_ROOT,
        "processed_data",
        "mandi_price_ml_features.csv"
    )

    feature_engineering(INPUT_FILE, OUTPUT_FILE)
