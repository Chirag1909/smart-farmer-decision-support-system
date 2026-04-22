import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

API_KEY = "9809ac00cd0f719f6bb4f02ca140c36a"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@router.get("/weather")
def get_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rainfall": data.get("rain", {}).get("1h", 0),
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }
