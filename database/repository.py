from database.connection import SessionLocal
from database.model import Trip


class TripRepository:

    def create_trip(
            self,
            destination: str,
            days: int,
            travelers: int,
            budget: float,
            status: str,
    ):
        db = SessionLocal()

        try:
            trip = Trip(
                destination=destination,
                days=days,
                travelers=travelers,
                budget=budget,
                status=status,
            )

            db.add(trip)
            db.commit()
            db.refresh(trip)

            return trip

        finally:
            db.close()


trip_repository = TripRepository()
