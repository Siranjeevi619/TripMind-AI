

from app.ai.llm import llm


async def chat(request: str) -> str:
    result = await llm.ainvoke(request)
    return str(result.content)

