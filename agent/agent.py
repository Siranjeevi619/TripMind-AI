import os

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq

from api.schema.trip import TripPlan
from tools.weather import get_weather

load_dotenv()

tools = [get_weather]

tools_map = {
    tool.name: tool
    for tool in tools
}

model = os.getenv("GROQ_MODEL")
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model=model, api_key=api_key, temperature=0.5)

llm_with_tools = llm.bind_tools(tools)

structured_llm = llm.with_structured_output(TripPlan)

SYSTEM_PROMPT = """
You are TripMind, an AI travel assistant.

Use available tools whenever they are needed.

Never invent information that can be obtained from a tool.

If a tool fails, clearly report the failure.
"""


def run_agent(user_question: str, llm_with_tools=None) -> TripPlan:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_question),
    ]

    max_iterations = 10

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            tool = tools_map[tool_call["name"]]

            result = tool.invoke(tool_call)

            messages.append(
                ToolMessage(
                    content=result.content,
                    tool_call_id=tool_call["id"],
                )
            )

    return "The agent could not complete the request."
