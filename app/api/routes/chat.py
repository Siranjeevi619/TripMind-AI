from urllib.request import Request

from fastapi import APIRouter

from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    try:
        response = await chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise e

