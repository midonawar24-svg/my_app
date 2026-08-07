from fastapi import FastAPI
from app.api.v1 import health

app = FastAPI(title="AI Core OS", version="0.1.0")

app.include_router(health.router, prefix="/api/v1", tags=["health"])

@app.get("/")
def root():
    return {"status": "AI Core OS Running"}
