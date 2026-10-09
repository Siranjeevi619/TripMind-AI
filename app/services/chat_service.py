from uuid import UUID

from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.orm import Session

from app.ai.llm import llm
from app.ai.prompts.chat import chat_prompt
from app.db.repositories import conversation_repository as repo


async def chat(message: str,db: Session,conversation_id: UUID | None = None) -> tuple[str, UUID]:
    if conversation_id is None:
        conversation = repo.create_conversation(db)
        conversation_id = conversation.id
    else:
        conversation = repo.get_conversation(db, conversation_id)
        if conversation is None:
            raise ValueError("Conversation not found")

    history = repo.get_recent_messages(
        db,
        conversation_id,
        limit=20,
    )

    repo.save_message(
        db,
        conversation_id,
        "user",
        message,
    )

    prompt_history = [
        HumanMessage(content=item.content)
        if item.role == "user"
        else AIMessage(content=item.content)
        for item in history
        if item.role in {"user", "assistant"}
    ]

    prompt_value = chat_prompt.invoke({
        "message": message,
        "history": prompt_history,
    })

    try:
        result = await llm.ainvoke(prompt_value)
        response = str(result.content)
    except Exception:
        raise

    repo.save_message(
        db,
        conversation_id,
        "assistant",
        response,
    )

    return response, conversation_id