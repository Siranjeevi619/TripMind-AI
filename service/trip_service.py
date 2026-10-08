import logging
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from agent.trip_agent import trip_agent
from api.schema.trip import TripRequest, TripResponse
from database.connection import SessionLocal
from database.plan_repository import trip_plan_repository
from database.repository import trip_repository

logger = logging.getLogger(__name__)


def process_trip(
        trip_id: int,
        destination: str,
        days: int,
        travelers: int,
        budget: float,
):
    """
    Background worker function that runs the AI agent workflow.
    Uses its own isolated database session rather than the HTTP request's session.
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting background AI processing for trip {trip_id} ({destination})")

        # 1. Run AI LangGraph Agent / tools workflow
        result = trip_agent.run(
            destination=destination,
            days=days,
            travelers=travelers,
            budget=budget,
        )

        # 2. Save the generated TripPlan
        trip_plan_repository.create_plan(
            db=db,
            trip_id=trip_id,
            weather=result.weather,
            places=result.places,
            itinerary=[
                day.model_dump() if hasattr(day, "model_dump") else day
                for day in result.itinerary
            ],
        )

        # 3. Mark status as completed
        trip_repository.update_status(db=db, trip_id=trip_id, status="completed")
        db.commit()
        logger.info(f"Successfully completed trip {trip_id}")

    except Exception as e:
        logger.error(f"Error processing trip {trip_id}: {e}", exc_info=True)
        db.rollback()
        try:
            trip_repository.update_status(db=db, trip_id=trip_id, status="failed")
            db.commit()
        except Exception as update_err:
            logger.error(f"Failed to update trip {trip_id} status to failed: {update_err}")
            db.rollback()
    finally:
        db.close()


class TripService:

    def create_trip(
            self,
            db: Session,
            request: TripRequest,
            background_tasks: BackgroundTasks,
    ) -> TripResponse:
        try:
            # 1. Create Trip record in PostgreSQL with status "processing"
            trip = trip_repository.create_trip(
                db=db,
                destination=request.destination,
                days=request.days,
                travelers=request.travelers,
                budget=request.budget,
                status="processing",
            )

            # 2. Commit transaction so it is persisted immediately
            db.commit()
            db.refresh(trip)

            # 3. Queue the AI workflow as a background task
            background_tasks.add_task(
                process_trip,
                trip_id=trip.id,
                destination=trip.destination,
                days=trip.days,
                travelers=trip.travelers,
                budget=trip.budget,
            )

            # 4. Return immediately to the client
            return TripResponse(
                trip_id=str(trip.id),
                destination=trip.destination,
                days=trip.days,
                travelers=trip.travelers,
                budget=trip.budget,
                status=trip.status,
            )

        except Exception:
            db.rollback()
            raise

    def get_trip(self, db: Session, trip_id: int) -> TripResponse | None:
        trip = trip_repository.get_trip(db=db, trip_id=trip_id)
        if trip is None:
            return None

        plan = trip.plan
        return TripResponse(
            trip_id=str(trip.id),
            destination=trip.destination,
            days=trip.days,
            travelers=trip.travelers,
            budget=trip.budget,
            status=trip.status,
            weather=plan.weather if plan else None,
            places=plan.places if plan else None,
            itinerary=plan.itinerary if plan else None,
        )


trip_service = TripService()
