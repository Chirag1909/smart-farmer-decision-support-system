from fastapi import APIRouter
from backend.services.weather_service import get_weather_data

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{state}")
def get_weather(state: str):
    return get_weather_data(state)

