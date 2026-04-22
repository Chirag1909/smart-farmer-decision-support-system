from fastapi import APIRouter
from backend.services.profit_service import get_profit_forecast

router = APIRouter(prefix="/profit", tags=["Profit Forecasting"])

@router.get("/{state}")
def get_profits(state: str):
    return get_profit_forecast(state)

