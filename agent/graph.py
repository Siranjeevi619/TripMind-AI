import json
import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode

from agent.state import TripState
from api.schema.trip import TripPlan
from tools.places import search_places
from tools.weather import get_weather

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

tools = [
    get_weather,
    search_places,
]

llm_with_tools = llm.bind_tools(tools)
structured_llm = llm.with_structured_output(TripPlan)

SYSTEM_PROMPT = """
        You are TripMind, an AI travel assistant.
        
        Your job is to create a complete travel plan.
        
        Use available tools whenever required.
        
        You must collect the information needed for the travel plan before finishing.
        
        For every trip:
        1. Get weather for the destination if weather is unavailable.
        2. Get recommended places if places are unavailable.
        3. After all required information is available, stop and allow the final planner to create the itinerary.
        
        Do not finish early after receiving only one tool result.
        
        Never invent information that can be obtained from a tool.
        
        If a tool fails, clearly report the failure.
        """


def final_planner_node(state: TripState):
    prompt = f"""
        Create the final travel itinerary.
        
        Destination: {state.destination}
        Days: {state.days}
        Travelers: {state.travelers}
        Budget: {state.budget}
        
        Weather:
        {state.weather}
        
        Places:
        {state.places}
        
        Rules:
        
        1. Create exactly {state.days} DayPlan objects.
        2. Each day must have the correct day number:
           Day 1, Day 2, ..., Day {state.days}.
        3. Every day must contain at least one activity.
        4. Use the available places when creating the itinerary.
        5. Do not invent places that are not provided.
        """

    result = structured_llm.invoke(prompt)

    return {
        "itinerary": result.itinerary
    }


def agent_node(state: TripState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state.messages,
    ]

    if not state.messages:
        messages.append(
            HumanMessage(
                content=f"""
            Create a travel plan for:
            
            Destination: {state.destination}
            Days: {state.days}
            Travelers: {state.travelers}
            Budget: {state.budget}
            
            Available weather:
            {state.weather}
            
            Available places:
            {state.places}
            """
            )
        )
    else:
        messages.append(
            HumanMessage(
                content=f"""
                    Continue working on the travel plan.
                    
                    Current state:
                    
                    Destination: {state.destination}
                    Days: {state.days}
                    Travelers: {state.travelers}
                    Budget: {state.budget}
                    
                    Weather:
                    {state.weather}
                    
                    Places:
                    {state.places}
                    
                    Check whether any required information is still missing.
                    If information is missing, use the appropriate tool.
                    If all required information is available, stop.
                    """
            )
        )

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


def update_state(state: TripState):
    updates = {}
    for message in state.messages:
        if message.type != "tool":
            continue
        if not isinstance(message.content, str):
            continue
        try:
            data = json.loads(message.content)
        except json.JSONDecodeError:
            continue
        for key, value in data.items():
            if hasattr(state, key):
                updates[key] = value

    return updates


def should_continue(state: TripState):
    last_message = state.messages[-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


builder = StateGraph(TripState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_node("update_state", update_state)
builder.add_node("final_planner", final_planner_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": "final_planner",
    },
)

builder.add_edge("tools", "update_state")
builder.add_edge("update_state", "agent")
builder.add_edge("final_planner", END)

graph = builder.compile()

if __name__ == "__main__":
    state = TripState(
        destination="Tokyo",
        days=3,
        travelers=2,
        budget=1000,
    )

    print("\n===== LANGGRAPH =====")
    print(graph.get_graph().draw_mermaid())

    result = graph.invoke(state)

    print("\n===== FINAL RESULT =====")
    print(result)
