from uuid import UUID

from fastapi import APIRouter, Depends
from requests import Session

from app.db.models.dependencies import get_db
from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        response, conversation_id = await chat(
            message=request.message,
            db=db,
            conversation_id=(
                UUID(request.conversation_id)
                if request.conversation_id
                else None
            )
        )

        return ChatResponse(
            response=response,
            conversation_id=str(conversation_id),
        )
    except Exception as e:
        raise e
