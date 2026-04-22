import os
from functools import lru_cache

import pandas as pd
import requests


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
WEATHER_DATA_PATH = os.path.join(BASE_DIR, "processed_data", "weather_cleaned.csv")


@lru_cache(maxsize=1)
def _load_state_coordinates():
    frame = pd.read_csv(WEATHER_DATA_PATH)
    frame["state_key"] = frame["state"].str.lower().str.strip()
    return frame[["state", "state_key", "latitude", "longitude"]]


def _get_coordinates(state: str):
    frame = _load_state_coordinates()
    row = frame[frame["state_key"] == state.lower().strip()]
    if row.empty:
        return None
    first = row.iloc[0]
    return float(first["latitude"]), float(first["longitude"])


def _from_openweather(state: str, api_key: str):
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": f"{state},IN", "appid": api_key, "units": "metric"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "source": "openweather",
    }


def _from_open_meteo(state: str):
    coords = _get_coordinates(state)
    if not coords:
        return {"error": f"No coordinates available for state '{state}'"}

    latitude, longitude = coords
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json().get("current", {})

    weather_code = int(data.get("weather_code", -1))
    weather_label = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "rime fog",
        51: "light drizzle",
        61: "light rain",
        63: "moderate rain",
        65: "heavy rain",
        71: "light snow",
        80: "rain showers",
        95: "thunderstorm",
    }.get(weather_code, f"weather code {weather_code}")

    return {
        "temperature": data.get("temperature_2m"),
        "humidity": data.get("relative_humidity_2m"),
        "condition": weather_label,
        "wind_speed": data.get("wind_speed_10m"),
        "source": "open-meteo",
    }


def _forecast_from_open_meteo(state: str):
    coords = _get_coordinates(state)
    if not coords:
        return {"error": f"No coordinates available for state '{state}'"}

    latitude, longitude = coords
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "forecast_days": 7,
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()
    daily = response.json().get("daily", {})

    forecast = []
    dates = daily.get("time", [])
    max_t = daily.get("temperature_2m_max", [])
    min_t = daily.get("temperature_2m_min", [])
    rain = daily.get("precipitation_sum", [])
    for idx in range(min(len(dates), len(max_t), len(min_t), len(rain))):
        forecast.append(
            {
                "date": dates[idx],
                "temp_max": max_t[idx],
                "temp_min": min_t[idx],
                "rainfall_mm": rain[idx],
            }
        )
    return {"forecast": forecast}


def get_weather(state: str):
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    try:
        current = _from_openweather(state, api_key) if api_key else _from_open_meteo(state)
    except Exception:
        try:
            current = _from_open_meteo(state)
        except Exception as exc:
            return {"error": f"Unable to fetch weather from providers: {str(exc)}"}

    # Add 7-day rainfall and temperature forecast for weather charts.
    try:
        forecast_payload = _forecast_from_open_meteo(state)
        if "forecast" in forecast_payload:
            forecast = forecast_payload["forecast"]
            rainfall_values = [row.get("rainfall_mm", 0) or 0 for row in forecast]
            current["forecast"] = forecast
            current["rainfall_summary"] = {
                "next_7_days_total_mm": round(sum(rainfall_values), 2),
                "next_7_days_avg_mm": round(sum(rainfall_values) / len(rainfall_values), 2) if rainfall_values else 0.0,
                "max_daily_mm": round(max(rainfall_values), 2) if rainfall_values else 0.0,
            }
    except Exception:
        current["forecast"] = []
        current["rainfall_summary"] = {
            "next_7_days_total_mm": 0.0,
            "next_7_days_avg_mm": 0.0,
            "max_daily_mm": 0.0,
        }

    return current
