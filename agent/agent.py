import os

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq

from agent.state import TripState
from api.schema.trip import TripPlan
from tools.places import search_places
from tools.weather import get_weather

load_dotenv()

tools = [get_weather, search_places]

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


def run_agent(user_question: str, state: TripState) -> TripPlan:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_question),
    ]

    max_iterations = 3

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:
            tool = tools_map[tool_call["name"]]

            result = tool.invoke(tool_call["args"])

            if isinstance(result, dict):
                for key, value in result.items():
                    if hasattr(state, key):
                        setattr(state, key, value)

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )
    trip_plan = structured_llm.invoke(messages)

    return trip_plan
