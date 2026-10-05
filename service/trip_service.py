from agent.agent import run_agent
from api.schema.trip import TripRequest, TripResponse


class TripService:
    def create_trip(self, request: TripRequest) -> TripResponse:
        prompt = f"""
                Create a travel plan for:

                Destination: {request.destination}
                Days: {request.days}
                Travelers: {request.travelers}
                Budget: ${request.budget}
                """

        result = run_agent(prompt)

        return TripResponse(
            trip_id="demo-123",
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
            status="created",
        )


trip_service = TripService()
