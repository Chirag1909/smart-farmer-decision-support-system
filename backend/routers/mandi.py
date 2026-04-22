from fastapi import APIRouter
from backend.services.mandi_service import forecast_price

router = APIRouter(prefix="/mandi", tags=["Mandi"])

@router.get("/")
def get_price(state: str, district: str, crop: str):
    return forecast_price(state, district, crop)