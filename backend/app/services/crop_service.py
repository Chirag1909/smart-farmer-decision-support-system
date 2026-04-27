import pandas as pd
import joblib
from config import DATA_DIR, MODEL_DIR

def _load_crop_df():
    path = DATA_DIR / "crop_dataset.csv"
    if not path.exists():
        return None
    frame = pd.read_csv(path)
    frame.columns = frame.columns.str.lower()
    return frame


def _load_model():
    path = MODEL_DIR / "crop_model.pkl"
    if not path.exists():
        return None
    return joblib.load(path)

def get_top_crops(state, district):
    crop_df = _load_crop_df()
    model = _load_model()
    if crop_df is None or model is None:
        return {"message": "Model or dataset not available in configured paths"}

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