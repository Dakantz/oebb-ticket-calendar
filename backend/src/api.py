from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from . import config
from .auth import router as auth_router
from .db import Booking, SessionLocal, User, init_db
from .gmail import fetch_bookings
from .ics import build_ics

app = FastAPI(title="oebb-ticket-calendar")
app.add_middleware(SessionMiddleware, secret_key=config.SESSION_SECRET, same_site="lax")
app.include_router(auth_router)

init_db()

CACHE_TTL = timedelta(minutes=10)
# ponytail: single-process cache; move to a DB column if the app ever runs multi-worker
_last_fetch: dict[str, datetime] = {}


def _refresh_bookings(db: Session, user: User) -> None:
    legs = fetch_bookings(user.refresh_token)
    db.query(Booking).filter_by(user_id=user.id).delete()
    db.add_all(Booking.from_leg(user.id, leg) for leg in legs)
    db.commit()
    _last_fetch[user.id] = datetime.now(timezone.utc)


@app.get("/backend/calendar/{calendar_token}.ics")
def calendar(calendar_token: str):
    with SessionLocal() as db:
        user = db.query(User).filter_by(calendar_token=calendar_token).one_or_none()
        if user is None or not user.refresh_token:
            raise HTTPException(404, "unknown calendar")

        last = _last_fetch.get(user.id)
        if last is None or datetime.now(timezone.utc) - last > CACHE_TTL:
            _refresh_bookings(db, user)

        legs = [b.to_leg() for b in db.query(Booking).filter_by(user_id=user.id)]

    return PlainTextResponse(build_ics(legs), media_type="text/calendar")
