from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from schemas.room import RoomOut


class BookingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    day: date
    slot: int = Field(ge=1, le=8)
    room_id: int = Field(gt=0)


class BookingOut(BaseModel):
    id: int
    title: str
    day: date
    slot: int
    user_id: int
    room: RoomOut
    model_config = ConfigDict(from_attributes=True)
