from api.schema.Trip import TripRequest, TripResponse


class TripService:
    def create_trip(self, request: TripRequest) -> TripResponse:
        return TripResponse(
            trip_id="001",
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
            status="Created"
        )


trip_service = TripService()
