from database.model import Trip


class TripRepository:

    def create_trip(
            self,
            db,
            destination: str,
            days: int,
            travelers: int,
            budget: float,
            status: str,
    ):
        trip = Trip(
            destination=destination,
            days=days,
            travelers=travelers,
            budget=budget,
            status=status,
        )

        db.add(trip)
        db.flush()

        return trip

    def get_trip(self, db, trip_id: int) -> Trip | None:
        return db.get(Trip, trip_id)

    def update_status(self, db, trip_id: int, status: str):
        trip = db.get(Trip, trip_id)

        if trip is None:
            raise ValueError(f"Trip {trip_id} not found")

        trip.status = status

        db.flush()

        return trip


trip_repository = TripRepository()
