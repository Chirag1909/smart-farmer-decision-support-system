from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import recommendation, mandi, weather

app = FastAPI(title="Crop Decision System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommendation.router)
app.include_router(mandi.router)
app.include_router(weather.router)