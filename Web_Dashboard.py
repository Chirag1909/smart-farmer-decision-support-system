# ======================================================
# IMPORTS
# ======================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="Farmer Dashboard", layout="wide")

# ======================================================
# CLEAN WHITE UI (RESEARCH PAPER FRIENDLY)
# ======================================================
st.markdown("""
<style>

/* Background */
body, .main {
    background-color: #ffffff;
    color: #1f2937;
}

/* Title */
.title {
    font-size: 40px;
    font-weight: bold;
    color: #2563eb;
}

/* Cards */
.card {
    background: #f9fafb;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    text-align: center;
    color: #111827;
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* Metrics */
.metric {
    font-size: 26px;
    font-weight: bold;
    color: #059669;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f3f4f6;
}

/* Buttons */
button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================
st.markdown('<div class="title">🌾 Smart Farmer Dashboard</div>', unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================
ranking_df = pd.read_csv("processed_data/best_crop_mandi_ranking.csv")
mandi_df = pd.read_csv("processed_data/cleaned_mandi_prices.csv")

ranking_df.columns = ranking_df.columns.str.lower()
mandi_df.columns = mandi_df.columns.str.lower()

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("📊 Dashboard Menu")

page = st.sidebar.radio(
    "Go to",
    ["Crop Recommendation", "Profit Analysis", "Market & Weather"]
)

state = st.sidebar.selectbox(
    "Select State",
    sorted(ranking_df["state"].dropna().unique())
)

# ======================================================
# FILTER DATA
# ======================================================
state_data = ranking_df[
    ranking_df["state"].str.lower() == state.lower()
]

top5 = state_data.sort_values("rank").head(5)

# ======================================================
# PAGE 1 - CROP RECOMMENDATION
# ======================================================
if page == "Crop Recommendation":

    st.subheader("🌱 Top Crop Suggestions")

    st.dataframe(top5, use_container_width=True)

# ======================================================
# PAGE 2 - PROFIT ANALYSIS
# ======================================================
elif page == "Profit Analysis":

    PRODUCTION_COST = 1500

    results = []

    for _, row in top5.iterrows():
        crop = row["crop"]
        yield_val = row["predicted_yield"]
        price = row["modal_price"]

        revenue = yield_val * price
        cost = yield_val * PRODUCTION_COST
        profit = revenue - cost
        margin = (profit / revenue) * 100 if revenue != 0 else 0

        results.append([crop, price, revenue, profit, margin])

    profit_df = pd.DataFrame(
        results,
        columns=["crop","forecast_price","expected_revenue","expected_profit","profit_margin_%"]
    )

    profit_df = profit_df.sort_values("expected_profit", ascending=False)

    best = profit_df.iloc[0]

    # CARDS
    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="card">🏆 Best Crop<br><div class="metric">{best["crop"]}</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">💰 Profit<br><div class="metric">₹ {round(best["expected_profit"],2)}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">📈 Margin<br><div class="metric">{round(best["profit_margin_%"],2)}%</div></div>', unsafe_allow_html=True)

    st.subheader("📊 Profit Table")
    st.dataframe(profit_df, use_container_width=True)

    # GRAPH
    st.subheader("📉 Profit Visualization")

    plt.figure()
    plt.plot(profit_df["crop"], profit_df["expected_profit"], marker="o")
    plt.title("Profit Comparison")
    plt.xlabel("Crop")
    plt.ylabel("Profit")
    plt.grid(True)

    st.pyplot(plt)

# ======================================================
# PAGE 3 - MARKET & WEATHER
# ======================================================
elif page == "Market & Weather":

    # ================= MANDI =================
    mandi_state = mandi_df[
        mandi_df["state"].str.lower() == state.lower()
    ]

    if not mandi_state.empty:

        best_mandi = mandi_state.sort_values("modal_price", ascending=False).iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.markdown(f'<div class="card">🏬 Market<br><div class="metric">{best_mandi["market"]}</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="card">🌾 Crop<br><div class="metric">{best_mandi["crop"]}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="card">💸 Price<br><div class="metric">₹ {best_mandi["modal_price"]}</div></div>', unsafe_allow_html=True)

    else:
        st.warning("No mandi data available")

    # ================= WEATHER =================
    st.subheader("🌦 Weather Overview")

    API_KEY = "9809ac00cd0f719f6bb4f02ca140c36a"   # <-- PUT YOUR KEY HERE

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={state},IN&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response["cod"] == 200:
            temp = response["main"]["temp"]
            humidity = response["main"]["humidity"]
            condition = response["weather"][0]["description"]
        else:
            temp, humidity, condition = "N/A", "N/A", "N/A"

    except:
        temp, humidity, condition = "N/A", "N/A", "N/A"

    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="card">🌡 Temperature<br><div class="metric">{temp} °C</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">💧 Humidity<br><div class="metric">{humidity}%</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">☁ Condition<br><div class="metric">{condition}</div></div>', unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.write("🚀 Smart Agriculture Decision Support System")