from fastapi import APIRouter, Query
from backend.services.crop_service import get_top_crops

router = APIRouter(prefix="/recommendation", tags=["Crop Recommendation"])

@router.get("/")
def recommend_crops(
    state: str = Query(..., description="State name"),
    district: str = Query(..., description="District name")
):
    return get_top_crops(state, district)

