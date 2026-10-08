from api.schema.trip import TripRequest, TripResponse
from database.repository import trip_repository


# class TripService:
#     def create_trip(self, request: TripRequest) -> TripResponse:
#         state = TripState(
#             destination=request.destination,
#             days=request.days,
#             travelers=request.travelers,
#             budget=request.budget,
#         )
# 
#         prompt = f"""
#                 Create a travel plan for:
# 
#                 Destination: {request.destination}
#                 Days: {request.days}
#                 Travelers: {request.travelers}
#                 Budget: ${request.budget}
#                 """
# 
#         result = run_agent(prompt, state=state)
# 
#         return TripResponse(
#             trip_id="demo-123",
#             destination=result.destination,
#             days=request.days,
#             travelers=request.travelers,
#             itinerary=result.itinerary,
#             budget=request.budget,
#             places=state.places,
#             weather=state.weather,
#             status="created",
#         )
#

class TripService:

    def create_trip(self, request: TripRequest):
        trip = trip_repository.create_trip(
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
            status="created",
        )

        return TripResponse(
            trip_id=str(trip.id),
            destination=trip.destination,
            days=trip.days,
            travelers=trip.travelers,
            budget=trip.budget,
            status=trip.status,
        )


trip_service = TripService()
