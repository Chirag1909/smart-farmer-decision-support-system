from fastapi import APIRouter
from backend.services.ranking_service import get_crop_ranking

router = APIRouter(prefix="/ranking", tags=["Ranking"])

@router.get("/{state}")
def get_rankings(state: str):
    return get_crop_ranking(state)

