import os

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()


@tool
def search_places(city: str) -> dict:
    """Find popular places to visit in a city."""

    places = {
        "Tokyo": [
            "Senso-ji Temple",
            "Shibuya Crossing",
            "Meiji Shrine",
            "Tokyo Skytree",
        ],
        "Paris": [
            "Eiffel Tower",
            "Louvre Museum",
            "Arc de Triomphe",
        ],
    }

    return {
        "city": city,
        "places": places.get(city, []),
    }


@tool
def calculate_budget(days: int, travelers: int, daily_budget: float) -> dict:
    """Calculate the total travel budget."""

    total = days * travelers * daily_budget

    return {
        "days": days,
        "travelers": travelers,
        "daily_budget": daily_budget,
        "total_budget": total,
    }


tools = [get_weather, search_places, calculate_budget]

tools_map = {
    tool.name: tool
    for tool in tools
}

llm = ChatGroq(model=os.getenv("GROQ_MODEL"),
               api_key=os.getenv("GROQ_API_KEY"), temperature=0.5)
llm_with_tool = llm.bind_tools(tools)

user_question = """I'm visiting Tokyo for 5 days with 2 people.
        My daily budget is $100 per person.
        Find places to visit, check the weather,
        and calculate my total budget."""

messages = [
    SystemMessage(
        content="""
        You are a travel assistant.

        Use the available tools whenever they are needed
        to answer the user's request.

        For places, use search_places.
        For weather, use get_weather.
        For budget calculations, use calculate_budget.

        Never invent information that can be obtained from a tool.

        If a tool returns an error, clearly explain the error
        and do not fabricate the missing information.
        """
    ),
    HumanMessage(content=user_question),
]
MAX_ITERATIONS = os.getenv("TOOL_MAX_ITERATIONS")
for i in range(MAX_ITERATIONS):
    response = llm_with_tool.invoke(messages)
    print(f"response tool calling -> {response}")
    messages.append(response)

    if not response.tool_calls:
        print("\nAI:")
        print(response.content)
        break

    for tool_call in response.tool_calls:
        tool = tools_map[tool_call["name"]]

        result = tool.invoke(tool_call)

        messages.append(
            ToolMessage(
                content=result.content,
                tool_call_id=tool_call["id"],
            )
        )
    final_response = llm_with_tool.invoke(messages)
    print("\nAI:")
    print(final_response.content)
