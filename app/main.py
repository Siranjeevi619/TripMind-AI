from fastapi import FastAPI

from app.api.routes.chat import router as chat_router

app = FastAPI()
app.include_router(chat_router)
@app.get("/health")
async def hello() -> dict[str, str]:
    return {"status": "ok"}