from fastapi import APIRouter
from backend.services.crop_service import get_top_crops

router = APIRouter(prefix="/recommendation", tags=["Crop"])

@router.get("/")
def recommend(state: str, district: str):
    return get_top_crops(state, district)