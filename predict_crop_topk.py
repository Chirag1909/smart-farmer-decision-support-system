import joblib
import pandas as pd
import numpy as np
import os

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "crop_recommendation_model_topk.pkl"
)

# ---------------- LOAD MODEL ----------------
bundle = joblib.load(MODEL_PATH)

model = bundle["model"]
label_encoder = bundle["label_encoder"]
feature_columns = bundle["feature_columns"]

# ---------------- PREDICTION FUNCTION ----------------
def recommend_crops_topk(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall,
    soil_type,
    k=5
):
    """
    Returns Top-K crop recommendations with probabilities
    """

    input_data = pd.DataFrame([{
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
        "soil_type": soil_type
    }])

    # Predict probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Get top-k indices
    top_k_idx = np.argsort(probabilities)[-k:][::-1]

    # Decode crop names
    crops = label_encoder.inverse_transform(top_k_idx)

    results = []
    for crop, idx in zip(crops, top_k_idx):
        results.append({
            "crop": crop,
            "probability": round(probabilities[idx], 4)
        })

    return results

# ---------------- DEMO RUN ----------------
if __name__ == "__main__":

    print("\n🔹 Sample Crop Recommendation 🔹\n")

    recommendations = recommend_crops_topk(
        nitrogen=90,
        phosphorus=42,
        potassium=43,
        temperature=26.5,
        humidity=80,
        ph=6.5,
        rainfall=200,
        soil_type="Loamy",
        k=5
    )

    for i, rec in enumerate(recommendations, start=1):
        print(f"{i}. {rec['crop']} (probability: {rec['probability']})")
