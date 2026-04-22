from fastapi import APIRouter, Query
from backend.services.mandi_service import forecast_price

router = APIRouter(prefix="/mandi", tags=["Mandi Prices"])

@router.get("/forecast")
def get_price_forecast(
    state: str = Query(...),
    district: str = Query(...),
    crop: str = Query(...)
):
    return forecast_price(state, district, crop)

