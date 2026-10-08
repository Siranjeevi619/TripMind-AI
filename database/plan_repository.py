from database.model import TripPlan

from database.connection import SessionLocal


class TripPlanRepository:

    def create_plan(
            self,
            trip_id: int,
            weather: dict | None,
            places: list | None,
            itinerary: list | None,
    ):
        db = SessionLocal()

        try:
            plan = TripPlan(
                trip_id=trip_id,
                weather=weather,
                places=places,
                itinerary=itinerary,
            )

            db.add(plan)
            db.commit()
            db.refresh(plan)

            return plan

        finally:
            db.close()


trip_plan_repository = TripPlanRepository()
