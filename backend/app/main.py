from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import mandi, recommendation, weather

app = FastAPI(title="Crop Decision System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommendation.router)
app.include_router(mandi.router)
app.include_router(weather.router)


@app.get("/health")
def health():
    return {"status": "ok"}
