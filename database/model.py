from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    destination: Mapped[str] = mapped_column(String(100))
    days: Mapped[int] = mapped_column(Integer)
    travelers: Mapped[int] = mapped_column(Integer)
    budget: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    plan: Mapped["TripPlan | None"] = relationship(
        back_populates="trip",
        uselist=False,
    )


class TripPlan(Base):
    __tablename__ = "trip_plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id"),
        nullable=False,
        unique=True,
    )

    weather: Mapped[dict | None] = mapped_column(JSON)
    places: Mapped[list | None] = mapped_column(JSON)
    itinerary: Mapped[list | None] = mapped_column(JSON)

    trip: Mapped["Trip"] = relationship(
        back_populates="plan"
    )
