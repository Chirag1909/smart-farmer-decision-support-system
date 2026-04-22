import pandas as pd
import os

# ---------------- CONFIG ---------------- #
YIELD_FILE = "processed_data/yield_predictions.csv"
PRICE_FILE = "crop_price_cost.csv"
OUTPUT_FILE = "processed_data/best_crop_mandi_ranking.csv"

# ---------------- FUNCTION ---------------- #
def rank_best_crops():
    print("Loading yield predictions...")
    yield_df = pd.read_csv(YIELD_FILE)
    print("Yield shape:", yield_df.shape)

    print("Loading mandi price dataset...")
    price_df = pd.read_csv(PRICE_FILE)
    print("Price shape:", price_df.shape)

    # ---------------- CLEAN COLUMN NAMES ---------------- #
    yield_df.columns = yield_df.columns.str.strip().str.lower()
    price_df.columns = price_df.columns.str.strip().str.lower()

    # ---------------- IDENTIFY PRICE COLUMN ---------------- #
    price_col = None
    for col in price_df.columns:
        if "modal" in col and "price" in col:
            price_col = col
            break

    if price_col is None:
        raise ValueError("Modal price column not found in crop_price_cost.csv")

    # ---------------- CLEAN CROP NAMES ---------------- #
    yield_df["crop_clean"] = (
        yield_df["crop"]
        .astype(str)
        .str.lower()
        .str.replace("type_", "", regex=False)
        .str.strip()
    )

    price_df["crop_clean"] = (
        price_df["commodity"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # ---------------- NUMERIC CONVERSION ---------------- #
    price_df[price_col] = pd.to_numeric(price_df[price_col], errors="coerce")
    yield_df["predicted_yield"] = pd.to_numeric(
        yield_df["predicted_yield"], errors="coerce"
    )

    price_df.dropna(subset=[price_col], inplace=True)
    yield_df.dropna(subset=["predicted_yield"], inplace=True)

    # ---------------- MERGE ---------------- #
    print("Merging yield and price data...")
    merged = pd.merge(
        price_df,
        yield_df,
        on="crop_clean",
        how="inner"
    )

    if merged.empty:
        raise ValueError("No crops matched between yield and price datasets")

    # ---------------- EXPECTED REVENUE ---------------- #
    merged["expected_revenue"] = (
        merged["predicted_yield"] * merged[price_col]
    )

    # ---------------- SELECT FINAL COLUMNS ---------------- #
    final_df = merged[
        ["state", "district", "commodity", "predicted_yield", price_col, "expected_revenue"]
    ].copy()

    final_df.rename(
        columns={
            "commodity": "crop",
            price_col: "modal_price"
        },
        inplace=True
    )

    # ---------------- RANKING ---------------- #
    final_df["rank"] = (
        final_df
        .groupby(["state", "district"])["expected_revenue"]
        .rank(method="dense", ascending=False)
    )

    final_df.sort_values(
        ["state", "district", "rank"],
        inplace=True
    )

    # ---------------- SAVE ---------------- #
    os.makedirs("processed_data", exist_ok=True)
    final_df.to_csv(OUTPUT_FILE, index=False)

    print("✅ Step 5 completed successfully")
    print("Saved to:", OUTPUT_FILE)

    # Show sample
    print("\nTop 5 sample recommendations:")
    print(final_df.head())

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    rank_best_crops()
