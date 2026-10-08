import uuid

from langchain_core.messages import HumanMessage, AIMessage

from app.ai.memory.store import conversation_store
from app.ai.prompts.chat import chat_prompt
from app.ai.llm import llm


async def chat(request: str, conversation_id : str) -> str:

    if  conversation_id is None:
        conversation_id = str(uuid.uuid4())

    history = conversation_store.setdefault(conversation_id, [])

    prompt_value = chat_prompt.invoke({
        "message":request,
        "history":history,
    })


    result = await llm.ainvoke(prompt_value)
    response =  str(result.content)

    history.extend([
        HumanMessage(content=request),
        AIMessage(content=response),
    ])
    return response, conversation_id

