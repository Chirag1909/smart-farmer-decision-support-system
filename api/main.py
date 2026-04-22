from fastapi import FastAPI
from api.weather_api import router as weather_router

app = FastAPI(
    title="Hydrology Crop Decision Support API",
    version="1.0"
)

@app.get("/")
def root():
    return {"status": "API running successfully"}

app.include_router(weather_router)
