from database.model import TripPlan


class TripPlanRepository:

    def create_plan(
            self,
            db,
            trip_id: int,
            weather: dict | None,
            places: list | None,
            itinerary: list | None,
    ):
        plan = TripPlan(
            trip_id=trip_id,
            weather=weather,
            places=places,
            itinerary=itinerary,
        )

        db.add(plan)
        db.flush()

        return plan


trip_plan_repository = TripPlanRepository()
