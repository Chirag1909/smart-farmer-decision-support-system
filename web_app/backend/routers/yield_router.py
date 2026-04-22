from fastapi import APIRouter
from backend.services.yield_service import get_yield_predictions

router = APIRouter(prefix="/yield", tags=["Yield Prediction"])

@router.get("/{state}")
def get_yields(state: str):
    return get_yield_predictions(state)

@router.get("/")
def get_all():
    return get_yield_predictions("")  # all

