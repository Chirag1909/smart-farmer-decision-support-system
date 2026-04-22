import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRICE_FILE = os.path.join(BASE_DIR, "crop_price_cost.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "processed_data", "filtered_crop_prices.csv")

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)


def fetch_mandi_prices(state, district, crop):

    if not os.path.exists(PRICE_FILE):
        raise FileNotFoundError(f"Price dataset not found: {PRICE_FILE}")

    print("Loading crop price–cost dataset...")
    df = pd.read_csv(PRICE_FILE)

    # -------------------------------------------------
    # NORMALIZE COLUMN NAMES
    # -------------------------------------------------
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

    required_cols = {
        "crop",
        "state",
        "district",
        "market_price"
    }

    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in price dataset: {missing}")

    # -------------------------------------------------
    # NORMALIZE TEXT VALUES
    # -------------------------------------------------
    df["crop"] = df["crop"].astype(str).str.lower().str.strip()
    df["state"] = df["state"].astype(str).str.lower().str.strip()
    df["district"] = df["district"].astype(str).str.lower().str.strip()

    # -------------------------------------------------
    # FILTER DATA
    # -------------------------------------------------
    filtered_df = df[
        (df["crop"] == crop.lower().strip()) &
        (df["state"] == state.lower().strip()) &
        (df["district"] == district.lower().strip())
    ]

    if filtered_df.empty:
        print("No price data found for given inputs.")
        return filtered_df

    # -------------------------------------------------
    # ENSURE NUMERIC
    # -------------------------------------------------
    filtered_df["market_price"] = pd.to_numeric(
        filtered_df["market_price"], errors="coerce"
    )

    # Save for downstream profit module
    filtered_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Filtered crop prices saved to: {OUTPUT_FILE}")
    return filtered_df


if __name__ == "__main__":
    STATE = "Maharashtra"
    DISTRICT = "Pune"
    CROP = "Wheat"

    result = fetch_mandi_prices(STATE, DISTRICT, CROP)

    if not result.empty:
        print(result[["crop", "market_price"]].head())
