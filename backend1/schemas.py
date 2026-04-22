from pydantic import BaseModel

class CropYield(BaseModel):
    crop: str
    predicted_yield: float

class ProfitRecommendation(BaseModel):
    crop: str
    predicted_yield: float
    modal_price: float
    net_profit: float
    profit_rank: int
