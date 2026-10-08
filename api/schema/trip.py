from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    destination: str = Field(min_length=2)
    days: int = Field(ge=1, le=30)
    travelers: int = Field(ge=1, le=20)
    budget: float = Field(gt=0)


class DayPlan(BaseModel):
    day: int
    activities: list[str]


class TripPlan(BaseModel):
    destination: str
    itinerary: list[DayPlan]


class TripResponse(BaseModel):
    trip_id: str
    destination: str
    days: int
    travelers: int
    budget: float
    status: str
    weather: dict | None = None
    places: list[str] | None = None
    itinerary: list[DayPlan] | None = None
