
from fastapi import FastAPI
from app.database import init_db

from app.players import router as players_router
from app.performances import router as performances_router
from app.auth import router as auth_router

app = FastAPI(title="Football Performance API")

# Initialize database
init_db()

# Include routers
app.include_router(players_router)
app.include_router(performances_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "API is running"}

