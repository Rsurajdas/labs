from datetime import date

from fastapi import APIRouter

from database import DB_DEPENDENCY
from dependencies import CurrentUser
from models.booking import Booking
from schemas.booking import BookingOut

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=list[BookingOut])
async def get_all_bookings(
    user: CurrentUser, db: DB_DEPENDENCY, day: date | None = None
):
    if day is not None:
        bookings = (
            db.query(Booking)
            .filter(Booking.user_id == user.id)
            .filter(Booking.day == day)
            .order_by(Booking.day.asc(), Booking.slot.asc())
            .all()
        )
    else:
        bookings = db.query(Booking).filter(Booking.user_id == user.id).all()

    return bookings
