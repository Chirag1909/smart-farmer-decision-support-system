import pandas as pd
import requests
from ..config import DATA_DIR

API_KEY = "9809ac00cd0f719f6bb4f02ca140c36a"

weather_df = pd.read_csv(DATA_DIR / "weather_cleaned.csv")

def get_weather_api(state: str):
    """Fetch real-time weather via OpenWeatherMap."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={state},IN&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()
        if data["cod"] == 200:
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"],
                "wind": data["wind"]["speed"]
            }
        return {"error": "Weather data not available"}
    except:
        return {"error": "API request failed"}

def get_weather_data(state: str):
    """Fallback to CSV summary."""
    df = weather_df[weather_df["state"].str.lower() == state.lower()]
    if df.empty:
        return get_weather_api(state)  # Try API
    summary = {
        "avg_temp": round(df["temperature"].mean(), 1),
        "avg_rainfall": round(df["rainfall"].mean(), 1),
        "days": df.shape[0],
        "source": "historical"
    }
    return summary


