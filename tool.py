import os

import requests
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()


@tool
def get_weather(city: str) -> dict:
    """
    Get the current weather for a city using a real weather API.
    """

    cities = {
        "Tokyo": {
            "latitude": 35.6762,
            "longitude": 139.6503,
        },
        "Paris": {
            "latitude": 48.8566,
            "longitude": 2.3522,
        },
        "London": {
            "latitude": 51.5074,
            "longitude": -0.1278,
        },
    }

    if city not in cities:
        return {
            "error": "City coordinates are not found",
        }

    api_url = os.getenv("WEATHER_API")

    params = {
        "latitude": cities[city]["latitude"],
        "longitude": cities[city]["longitude"],
        "current": "temperature_2m,weather_code",
    }

    max_retries = int(os.getenv("MAX_RETRIES"))
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Weather API attempt {attempt}/{max_retries}")
            response = requests.get(
                url=api_url,
                params=params,
                timeout=5,
            )
            response.raise_for_status()

            data = response.json()
            current_weather = data["current"]

            return {
                "city": city,
                "temperature": current_weather["temperature_2m"],
                "weather_code": current_weather["weather_code"],
            }


        except requests.RequestException as e:
            print(
                f"Weather API failed: {e}"
            )

            if attempt == max_retries:
                return {
                    "success": False,
                    "error": (
                        "Weather service is currently "
                        "unavailable after 3 attempts."
                    ),
                }
    return {
        "success": False,
        "error": "Unknown weather service error.",
    }


from langchain_core.tools import tool


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
        and calculate my total budget.
    """

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
while True:
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
