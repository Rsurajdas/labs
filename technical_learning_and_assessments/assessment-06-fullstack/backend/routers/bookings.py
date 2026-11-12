from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from database import DB_DEPENDENCY
from dependencies import CurrentUser
from models.booking import Booking
from models.room import Room
from schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=list[BookingOut], status_code=status.HTTP_200_OK)
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


@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(user: CurrentUser, db: DB_DEPENDENCY, body: BookingCreate):
    if db.query(Room).filter(Room.id == body.room_id).first() is None:
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


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking_bny_id(
    user: CurrentUser, db: DB_DEPENDENCY, booking_id: Annotated[int, Path(gt=0)]
):
    exiting_booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if exiting_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
        )

    if exiting_booking.user_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this booking",
        )

    db.delete(exiting_booking)
    db.commit()
