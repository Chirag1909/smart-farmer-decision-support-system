from fastapi import APIRouter
from ..services.states import get_states

router = APIRouter(prefix="/states", tags=["States"])

@router.get("/")
async def get_all_states():
    return {"states": get_states()}

