import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

ROOT_DIR = str(Path(__file__).resolve().parent.parent)
CURRENT_DIR = str(Path(__file__).resolve().parent)

if CURRENT_DIR in sys.path:
    sys.path.remove(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from agent.state import TripState

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

SYSTEM_PROMPT = """
    You are TripMind, an AI travel assistant.
    
    Use the available information in the state to help create a travel plan.
    Do not invent information that is not available.
    """


def agent_node(state: TripState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
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
        ),
    ]

    response = llm.invoke(messages)

    print("LLM:", response.content)

    return state


builder = StateGraph(TripState)

builder.add_node("agent", agent_node)

builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()

if __name__ == "__main__":
    state = TripState(
        destination="Tokyo",
        days=3,
        travelers=2,
        budget=1000,
    )

    result = graph.invoke(state)

    print(result)
