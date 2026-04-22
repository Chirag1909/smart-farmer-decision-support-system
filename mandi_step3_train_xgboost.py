import pandas as pd
import os
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor


def train_xgboost_model(input_file, model_output_path):
    print("Loading feature-engineered dataset...")

    df = pd.read_csv(input_file)
    print(f"Dataset shape: {df.shape}")

    # -------------------------
    # FEATURES & TARGET
    # -------------------------
    target = "modal_price"

    features = [
        "state_id", "district_id", "market_id", "crop_id",
        "year", "month", "week", "day",
        "day_of_week", "is_weekend",
        "price_lag_1", "price_lag_7", "price_lag_14",
        "rolling_mean_7", "rolling_mean_14"
    ]

    X = df[features]
    y = df[target]

    # -------------------------
    # TIME-BASED SPLIT
    # -------------------------
    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    print("Training samples:", X_train.shape[0])
    print("Testing samples:", X_test.shape[0])

    # -------------------------
    # XGBOOST MODEL
    # -------------------------
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1
    )

    print("Training XGBoost model...")
    model.fit(X_train, y_train)

    # -------------------------
    # EVALUATION
    # -------------------------
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print("\nModel Evaluation:")
    print(f"MAE  : ₹{mae:.2f}")
    print(f"RMSE : ₹{rmse:.2f}")

    # -------------------------
    # SAVE MODEL
    # -------------------------
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)

    print(f"\nModel saved at: {model_output_path}")


if __name__ == "__main__":

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    INPUT_FILE = os.path.join(
        PROJECT_ROOT,
        "processed_data",
        "mandi_price_ml_features.csv"
    )

    MODEL_OUTPUT = os.path.join(
        PROJECT_ROOT,
        "models",
        "mandi_price_xgboost.pkl"
    )

    train_xgboost_model(INPUT_FILE, MODEL_OUTPUT)
