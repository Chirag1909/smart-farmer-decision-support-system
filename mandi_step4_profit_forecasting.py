import pandas as pd
import os

# ---------------------------
# File paths
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

YIELD_FILE = os.path.join(BASE_DIR, "processed_data", "yield_predictions.csv")
PRICE_FILE = os.path.join(BASE_DIR, "crop_price_cost.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "processed_data", "profit_forecast.csv")


# ---------------------------
# Helper functions
# ---------------------------
def clean_crop_name(name):
    if pd.isna(name):
        return None
    name = str(name).lower()
    name = name.replace("type_", "")
    name = name.split("(")[0]
    return name.strip()


# ---------------------------
# Main logic
# ---------------------------
def profit_forecasting(yield_file, price_file, output_file):

    if not os.path.exists(yield_file):
        raise FileNotFoundError(f"Yield file not found: {yield_file}")

    if not os.path.exists(price_file):
        raise FileNotFoundError(f"Price file not found: {price_file}")

    print("Loading yield predictions...")
    yield_df = pd.read_csv(yield_file)
    print("Yield shape:", yield_df.shape)

    print("Loading crop price dataset...")
    price_df = pd.read_csv(price_file)
    print("Price shape:", price_df.shape)

    # ---------------------------
    # Normalize column names
    # ---------------------------
    price_df.columns = [c.strip() for c in price_df.columns]

    # ---------------------------
    # Detect modal price column
    # ---------------------------
    modal_price_col = None
    for col in price_df.columns:
        if "modal" in col.lower() and "price" in col.lower():
            modal_price_col = col
            break

    if modal_price_col is None:
        raise ValueError(
            f"No modal price column found. Available columns: {list(price_df.columns)}"
        )

    print(f"Using price column: {modal_price_col}")

    price_df[modal_price_col] = pd.to_numeric(
        price_df[modal_price_col], errors="coerce"
    )

    # ---------------------------
    # Crop name normalization
    # ---------------------------
    if "crop" not in yield_df.columns:
        raise ValueError("Yield file must contain 'crop' column")

    yield_df["crop_clean"] = yield_df["crop"].apply(clean_crop_name)

    # Detect crop column in price file
    price_crop_col = None
    for col in price_df.columns:
        if col.lower() in ["crop", "commodity", "crop_name"]:
            price_crop_col = col
            break

    if price_crop_col is None:
        raise ValueError(
            f"No crop column found in price file. Columns: {list(price_df.columns)}"
        )

    price_df["crop_clean"] = price_df[price_crop_col].apply(clean_crop_name)

    # ---------------------------
    # Merge yield & price
    # ---------------------------
    print("Merging yield and price data...")
    merged_df = pd.merge(
        yield_df,
        price_df,
        on="crop_clean",
        how="inner"
    )

    if merged_df.empty:
        raise ValueError("No crops matched between yield and price datasets")

    # ---------------------------
    # Profit calculation
    # ---------------------------
    merged_df["expected_revenue"] = (
        merged_df["predicted_yield"] * merged_df[modal_price_col]
    )

    final_cols = [
        "crop",
        "predicted_yield",
        modal_price_col,
        "expected_revenue"
    ]

    merged_df = merged_df[final_cols]

    # ---------------------------
    # Save output
    # ---------------------------
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    merged_df.to_csv(output_file, index=False)

    print("✅ Profit forecasting completed")
    print(f"Saved to: {output_file}")
    print("Sample output:")
    print(merged_df.head())


# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    profit_forecasting(YIELD_FILE, PRICE_FILE, OUTPUT_FILE)
