# GIVEN — do not change.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import booking, room, user  # noqa: F401  (registers the tables)
from routers import auth, bookings, rooms

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Room Booking API")

# Lets the Vite dev server (http://localhost:5173) call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
