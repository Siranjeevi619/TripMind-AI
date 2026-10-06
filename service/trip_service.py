from agent.agent import run_agent
from agent.state import TripState
from api.schema.trip import TripRequest, TripResponse


class TripService:
    def create_trip(self, request: TripRequest) -> TripResponse:
        state = TripState(
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
        )

        prompt = f"""
                Create a travel plan for:

                Destination: {request.destination}
                Days: {request.days}
                Travelers: {request.travelers}
                Budget: ${request.budget}
                """

        result = run_agent(prompt, state=state)

        return TripResponse(
            trip_id="demo-123",
            destination=result.destination,
            days=request.days,
            travelers=request.travelers,
            itinerary=result.itinerary,
            budget=request.budget,
            status="created",
        )


trip_service = TripService()
