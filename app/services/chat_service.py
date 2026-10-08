from app.ai.prompts.chat import chat_prompt
from app.ai.llm import llm


async def chat(request: str) -> str:
    prompt = chat_prompt.invoke(request)
    result = await llm.ainvoke(prompt)
    return str(result.content)

