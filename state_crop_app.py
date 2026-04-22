import os
import pandas as pd
import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(page_title="State Crop Recommendation", layout="centered")

st.title("🌾 State-Based Crop Recommendation System")

# ==========================================================
# LOAD DATA
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mandi_path = os.path.join(BASE_DIR, "processed_data", "best_crop_mandi_ranking.csv")

mandi_df = pd.read_csv(mandi_path)

# Clean columns
mandi_df["crop"] = mandi_df["crop"].astype(str).str.lower()
mandi_df["state"] = mandi_df["state"].astype(str).str.lower()
mandi_df["district"] = mandi_df["district"].astype(str)

# Get unique states
states = sorted(mandi_df["state"].unique())

# ==========================================================
# DROPDOWN
# ==========================================================

selected_state = st.selectbox("Select State", states)

# ==========================================================
# PROCESSING
# ==========================================================

if selected_state:

    state_data = mandi_df[mandi_df["state"] == selected_state]

    if state_data.empty:
        st.warning("No data found for selected state.")
    else:
        # Aggregate max revenue per crop
        crop_revenue = (
            state_data.groupby("crop")["expected_revenue"]
            .max()
            .reset_index()
            .sort_values(by="expected_revenue", ascending=False)
            .head(5)
        )

        st.subheader("Top 5 Crops")

        for i, row in crop_revenue.iterrows():

            crop_name = row["crop"]
            profit = row["expected_revenue"]

            # Get best mandi (rank = 1)
            best_mandi_row = state_data[
                (state_data["crop"] == crop_name) &
                (state_data["rank"] == 1)
            ]

            if not best_mandi_row.empty:
                best_mandi = best_mandi_row["district"].values[0]
            else:
                best_mandi = "Not Available"

            st.markdown(f"""
            ### 🌱 {crop_name.capitalize()}
            - **Expected Profit:** ₹{profit:,.2f}
            - **Best Mandi:** {best_mandi}, {selected_state.capitalize()}
            """)
