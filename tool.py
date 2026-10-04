import os

from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage
from langchain_core.tools import  tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city."""

    weather_data = {
        "Tokyo": {
            "temperature": 24,
            "condition": "Cloudy"
        },
        "Paris": {
            "temperature": 18,
            "condition": "Sunny"
        },
        "London": {
            "temperature": 15,
            "condition": "Rainy"
        },
    }

    return weather_data.get(
        city,
        {
            "temperature": 25,
            "condition": "Unknown"
        }
    )

@tool
def get_places(city: str) -> dict:
    """Get the Popular places for a city"""
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
            "Notre-Dame Cathedral",
            "Arc de Triomphe",
        ],
        "London": [
            "Big Ben",
            "Tower of London",
            "British Museum",
            "London Eye",
        ],
    }

    return places.get(city, ["No places found in the place"])

@tool
def calculate_budget(days : int , daily_budget:float) -> dict:
    """Calculate the estimated travel budget based on number of days and daily spending."""

    total = days * daily_budget

    return {
        "days": days,
        "daily_budget": daily_budget,
        "estimated_total": total,
    }

tools = [get_weather, get_places, calculate_budget]

llm = ChatGroq(model=os.getenv("GROQ_MODEL"),
               api_key= os.getenv("GROQ_API_KEY"), temperature=0.5)
llm_with_tool = llm.bind_tools(tools)
tool_map = {
    "get_places": get_places,
    "get_weather": get_weather,
    "calculate_budget": calculate_budget,
}
user_question = input("You: ")

messages = [
    SystemMessage(
        content="""
        You are a travel assistant.

        When answering using a tool result, use ONLY the information
        returned by the tool.

        Do not add places, facts or recommendations from your own
        knowledge if they were not returned by the tool.
        """
    ),
    HumanMessage(content=user_question),
]

response = llm_with_tool.invoke(messages)
print(f"response tool calling -> {response}")
messages.append(response)
if response.tool_calls :
    for tool_call in response.tool_calls:

        selected_tool = tool_map[
            tool_call["name"]
        ]
        result = selected_tool.invoke(
            tool_call
        )

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )
    final_response = llm_with_tool.invoke(messages)
    print("\nAI:")
    print(final_response)
else:
    print("\nAI:")
    print(response.content)
