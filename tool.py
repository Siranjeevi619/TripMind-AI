import os

from langchain_core.messages import ToolMessage, HumanMessage
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

tools = [get_weather]

llm = ChatGroq(model=os.getenv("GROQ_MODEL"),
               api_key= os.getenv("GROQ_API_KEY"), temperature=0.5)
llm_with_tool = llm.bind_tools(tools)

user_question = input("You: ")

messages = [
    HumanMessage(content=user_question),
]

response = llm_with_tool.invoke(messages)

if response.tool_calls:
    print(response.tool_calls)
    messages.append(response)
    for tool_call in response.tool_calls:
        tool_result = get_weather.invoke(tool_call)
        print("\nTool result:")
        print(tool_result)
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )
    final_response = llm_with_tool.invoke(messages)
    print("\nAI:")
    print(final_response.content)
else:
    print("\nAI:")
    print(response.content)
