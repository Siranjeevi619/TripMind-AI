import sys
from pathlib import Path
from typing import Annotated, List

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from pydantic import BaseModel, Field

from api.schema.trip import DayPlan


class TripState(BaseModel):
    destination: str
    days: int
    travelers: int
    budget: float

    weather: dict | None = None
    places: list[str] = Field(default_factory=list)
    itinerary: list[DayPlan] = Field(default_factory=list)

    messages: Annotated[List[AnyMessage], add_messages] = Field(default_factory=list)
