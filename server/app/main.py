from fastapi import FastAPI

from app.api.v1 import health, chat


app = FastAPI(title="AI Core OS", version="0.1.0")


# Versioned API
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["health"],
)

app.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["chat"],
)

# Compatibility routes used by the current Flutter client
app.include_router(
    health.router,
    prefix="",
    tags=["health-compat"],
)

app.include_router(
    chat.router,
    prefix="",
    tags=["chat-compat"],
)


@app.get("/")
def root():
    return {"status": "AI Core OS Running"}
