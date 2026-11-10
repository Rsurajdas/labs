# GIVEN — run once on an EMPTY database:  python seed.py
# Creates the admin account and three rooms. Needs Q1, Q2 and hash_password (Q3).
from database import Base, SessionLocal, engine
from models import booking, room, user  # noqa: F401
from models.room import Room
from models.user import User
from security import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    db.add(
        User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("adminpass123"),
            role="admin",
        )
    )
    db.add_all(
        [
            Room(name="Focus Pod", capacity=2),    # id 1
            Room(name="Board Room", capacity=10),  # id 2
            Room(name="Quiet Room", capacity=4),   # id 3
        ]
    )
    db.commit()
    print("Seeded: admin user (id 1) and rooms 1-3")
finally:
    db.close()
