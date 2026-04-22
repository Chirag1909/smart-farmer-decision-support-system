import pandas as pd
import joblib
from backend.config import DATA_DIR, MODEL_DIR

crop_df = pd.read_csv(DATA_DIR / "crop_dataset.csv")
crop_df.columns = crop_df.columns.str.lower()

model = joblib.load(MODEL_DIR / "crop_model.pkl")

def get_top_crops(state, district):

    df = crop_df.copy()

    df = df[
        (df["state"].str.lower() == state.lower()) &
        (df["district"].str.lower() == district.lower())
    ]

    if df.empty:
        return {"message": "No data found"}

    features = ["nitrogen", "phosphorus", "potassium",
                "rainfall", "temperature", "ph"]

    df["predicted_yield"] = model.predict(df[features])

    top5 = df.sort_values("predicted_yield", ascending=False).head(5)

    return top5[["crop", "predicted_yield"]].to_dict(orient="records")