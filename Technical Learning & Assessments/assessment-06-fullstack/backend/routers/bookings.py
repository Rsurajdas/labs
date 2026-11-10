from datetime import date

from fastapi import APIRouter, HTTPException
from starlette import status

from database import DB_DEPENDENCY
from dependencies import CurrentUser
from models.booking import Booking
from schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=list[BookingOut])
async def get_all_bookings(
    user: CurrentUser, db: DB_DEPENDENCY, day: date | None = None
):
    query = db.query(Booking)

    if user.role != "admin":
        query = query.filter(Booking.user_id == user.id)

    if day is not None:
        query = query.filter(Booking.day == day)

    bookings = query.order_by(Booking.day.asc(), Booking.slot.asc()).all()

    return bookings


@router.post("/", response_model=BookingOut)
async def create_booking(user: CurrentUser, db: DB_DEPENDENCY, body: BookingCreate):
    if body.room_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    exiting_booking = (
        db.query(Booking)
        .filter(Booking.room_id == body.room_id)
        .filter(Booking.day == body.day)
        .filter(Booking.slot == body.slot)
        .first()
    )

    if exiting_booking is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Slot already booked"
        )

    new_booking = Booking(
        title=body.title,
        day=body.day,
        slot=body.slot,
        room_id=body.room_id,
        user_id=user.id,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking
