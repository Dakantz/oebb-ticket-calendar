import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, ForeignKey, String, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DB_PATH = "sqlite:///./oebb.db"
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    google_sub: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String)
    calendar_token: Mapped[str] = mapped_column(
        String, unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    refresh_token: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    message_id: Mapped[str] = mapped_column(String)
    booking_code: Mapped[str] = mapped_column(String)
    from_station: Mapped[str] = mapped_column(String)
    to_station: Mapped[str] = mapped_column(String)
    person: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    link: Mapped[str] = mapped_column(String)

    def to_leg(self) -> dict:
        return {
            "message_id": self.message_id,
            "booking_code": self.booking_code,
            "from": self.from_station,
            "to": self.to_station,
            "person": self.person,
            "start": self.start_date,
            "end": self.end_date,
            "link": self.link,
        }

    @classmethod
    def from_leg(cls, user_id: str, leg: dict) -> "Booking":
        return cls(
            id=f"{leg['message_id']}-{leg['from']}-{leg['to']}-{leg['start']}",
            user_id=user_id,
            message_id=leg["message_id"],
            booking_code=leg["booking_code"],
            from_station=leg["from"],
            to_station=leg["to"],
            person=leg["person"],
            start_date=leg["start"],
            end_date=leg["end"],
            link=leg["link"],
        )


def init_db() -> None:
    Base.metadata.create_all(engine)
