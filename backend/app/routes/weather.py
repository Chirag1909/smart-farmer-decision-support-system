from fastapi import APIRouter
from app.services.weather_service import get_weather

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
def weather(state: str):
    return get_weather(state)