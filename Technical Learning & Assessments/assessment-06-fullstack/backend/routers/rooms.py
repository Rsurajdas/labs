# GIVEN — except the two TODOs for Q4. Change nothing else.
from fastapi import APIRouter, HTTPException, status

from database import DB_DEPENDENCY
from models.room import Room
from schemas.room import RoomCreate, RoomOut

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomOut])
def list_rooms(db: DB_DEPENDENCY):
    return db.query(Room).order_by(Room.id).all()


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: DB_DEPENDENCY):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


# TODO Q4: admin only
@router.post("", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(body: RoomCreate, db: DB_DEPENDENCY):
    if db.query(Room).filter(Room.name == body.name).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Room name already exists"
        )
    room = Room(name=body.name, capacity=body.capacity)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


# TODO Q4: admin only
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: DB_DEPENDENCY):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    db.delete(room)
    db.commit()
