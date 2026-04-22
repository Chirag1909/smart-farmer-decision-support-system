from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from .routers import recommendation, mandi, profit, yield_router, ranking, weather, auth, states
from .dependencies import get_current_user

app = FastAPI(title="Hydrology Crop Decision Support", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(states.router)
app.include_router(recommendation.router)
app.include_router(mandi.router)
app.include_router(profit.router)
app.include_router(yield_router.router)
app.include_router(ranking.router)
app.include_router(weather.router)

# Protected example
@app.get("/protected/dashboard")
async def protected_dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, welcome to dashboard"}

# Serve React build (prod)
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse("../frontend/build/index.html")

@app.get("/health")
def health():
    return {"status": "healthy", "version": "2.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

