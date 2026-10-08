from agent.trip_agent import trip_agent
from api.schema.trip import TripRequest, TripResponse
from database.plan_repository import trip_plan_repository
from database.repository import trip_repository


class TripService:

    def create_trip(self, request: TripRequest):
        trip = trip_repository.create_trip(
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
            status="processing",
        )

        result = trip_agent.run(
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
        )

        trip_plan_repository.create_plan(
            trip_id=trip.id,
            weather=result.weather,
            places=result.places,
            itinerary=[
                day.model_dump()
                for day in result.itinerary
            ],
        )

        return TripResponse(
            trip_id=str(trip.id),
            destination=trip.destination,
            days=trip.days,
            travelers=trip.travelers,
            weather=result.weather,
            budget=trip.budget,
            places=result.places,
            itinerary=result.itinerary,
            status="completed",
        )


trip_service = TripService()
