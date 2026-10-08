from urllib.request import Request

from fastapi import APIRouter
from pydantic.v1.typing import NoneType

from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    try:
        response, conversation_id = await chat(
            request=request.message,
            conversation_id=request.conversation_id
        )

        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
        )
    except Exception as e:
        raise e

