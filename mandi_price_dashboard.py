import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Mandi Price Intelligence Dashboard",
    layout="wide"
)

st.title("Mandi Price Intelligence Dashboard")
st.caption("Location-based mandi price analysis using Agmarknet data")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Agriculture_price_dataset.csv")
    df.columns = [c.strip() for c in df.columns]
    df["Price Date"] = pd.to_datetime(df["Price Date"], errors="coerce")
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

state_list = sorted(df["STATE"].dropna().unique())
state = st.sidebar.selectbox("State", state_list)

district_list = sorted(
    df[df["STATE"] == state]["District Name"].dropna().unique()
)
district = st.sidebar.selectbox("District", district_list)

market_list = sorted(
    df[
        (df["STATE"] == state) &
        (df["District Name"] == district)
    ]["Market Name"].dropna().unique()
)
market = st.sidebar.selectbox("Market", market_list)

commodity_list = sorted(
    df[
        (df["STATE"] == state) &
        (df["District Name"] == district) &
        (df["Market Name"] == market)
    ]["Commodity"].dropna().unique()
)
commodity = st.sidebar.selectbox("Commodity", commodity_list)

# -----------------------------
# Filter Data
# -----------------------------
filtered_df = df[
    (df["STATE"] == state) &
    (df["District Name"] == district) &
    (df["Market Name"] == market) &
    (df["Commodity"] == commodity)
].sort_values("Price Date")

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

latest = filtered_df.iloc[-1]

# -----------------------------
# Metrics
# -----------------------------
st.subheader("Latest Prices")

c1, c2, c3 = st.columns(3)
c1.metric("Min Price (₹/Quintal)", int(latest["Min_Price"]))
c2.metric("Max Price (₹/Quintal)", int(latest["Max_Price"]))
c3.metric("Modal Price (₹/Quintal)", int(latest["Modal_Price"]))

st.caption(f"Price Date: {latest['Price Date'].date()}")

# -----------------------------
# Trend Chart
# -----------------------------
st.subheader("Modal Price Trend")

fig, ax = plt.subplots()
ax.plot(filtered_df["Price Date"], filtered_df["Modal_Price"])
ax.set_xlabel("Date")
ax.set_ylabel("Modal Price (₹/Quintal)")
ax.grid(True)

st.pyplot(fig)

# -----------------------------
# Table
# -----------------------------
st.subheader("Historical Price Records")
st.dataframe(
    filtered_df[
        ["Price Date", "Min_Price", "Max_Price", "Modal_Price", "Variety", "Grade"]
    ].reset_index(drop=True)
)
