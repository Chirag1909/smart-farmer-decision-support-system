import os
import pandas as pd

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# LOAD DATA
# ==========================================================

mandi_path = os.path.join(BASE_DIR, "processed_data", "best_crop_mandi_ranking.csv")
mandi_df = pd.read_csv(mandi_path)

# ==========================================================
# CLEAN DATA
# ==========================================================

mandi_df["crop"] = mandi_df["crop"].astype(str).str.lower()
mandi_df["state"] = mandi_df["state"].astype(str).str.lower()

# ==========================================================
# FUNCTION: GET TOP 5 CROPS BY STATE
# ==========================================================

def get_top_5_crops_by_state(state_input):

    state_input = state_input.lower()

    # Filter data for selected state
    state_data = mandi_df[mandi_df["state"] == state_input]

    if state_data.empty:
        print("No data found for this state.")
        return []

    # Aggregate max revenue per crop within state
    crop_revenue = (
        state_data.groupby("crop")["expected_revenue"]
        .max()
        .reset_index()
    )

    # Sort by highest revenue
    crop_revenue = crop_revenue.sort_values(
        by="expected_revenue",
        ascending=False
    )

    # Select top 5 crops
    top_5_crops = crop_revenue.head(5)

    results = []

    for _, row in top_5_crops.iterrows():

        crop_name = row["crop"]

        # Get best mandi (rank = 1) for that crop in this state
        best_mandi_row = state_data[
            (state_data["crop"] == crop_name) &
            (state_data["rank"] == 1)
        ]

        if not best_mandi_row.empty:
            best_mandi = best_mandi_row["district"].values[0]
        else:
            best_mandi = "Not Available"

        results.append({
            "crop": crop_name,
            "expected_profit": row["expected_revenue"],
            "best_mandi": best_mandi + ", " + state_input
        })

    return results


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    state = input("Enter State: ")

    recommendations = get_top_5_crops_by_state(state)

    print("\n===== TOP 5 CROPS FOR YOUR STATE =====\n")

    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. Crop: {rec['crop']}")
        print(f"   Expected Profit: ₹{rec['expected_profit']:.2f}")
        print(f"   Best Mandi: {rec['best_mandi']}")
        print()
