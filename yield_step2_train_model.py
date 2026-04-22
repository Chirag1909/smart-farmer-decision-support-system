# yield_step2_train_model.py

import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

INPUT_FILE = "processed_data/yield_features.csv"
MODEL_OUTPUT = "models/yield_prediction_model.pkl"

def train_yield_model(input_file, model_output):
    print("Loading yield feature dataset...")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Feature file not found: {input_file}")

    df = pd.read_csv(input_file)
    print("Dataset shape:", df.shape)

    # Target variable
    TARGET = "yield"

    if TARGET not in df.columns:
        raise ValueError("Target column 'yield' not found in dataset")

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training samples:", X_train.shape[0])
    print("Testing samples:", X_test.shape[0])

    # Model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )

    print("Training Random Forest model...")
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    print("\nModel Evaluation:")
    print(f"MAE  : {mae:.2f} tons/hectare")
    print(f"RMSE : {rmse:.2f} tons/hectare")
    print(f"R²   : {r2:.3f}")

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, model_output)

    print("\nModel saved at:", model_output)

if __name__ == "__main__":
    train_yield_model(INPUT_FILE, MODEL_OUTPUT)
