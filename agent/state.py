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
