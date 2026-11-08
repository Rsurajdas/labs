from fastapi import APIRouter, HTTPException
from starlette import status

from database import DB_DEPENDENCY
from models.user import User
from schemas.auth import UserCreate, UserOut
from security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register(db: DB_DEPENDENCY, body: UserCreate):
    username = body.username.strip()
    email = body.email.strip().lower()

    exiting_username = db.query(User).filter(User.username == username).first()

    if exiting_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
        )

    exiting_email = db.query(User).filter(User.email == email).first()

    if exiting_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    new_user = {
        "username": username,
        "email": email,
        "password": hash_password(body.password),
        "role": "user",
        "is_active": True,
    }

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
        "is_active": new_user.is_active,
    }


#
# Q4 — authenticate_user(db, username, password)
#      POST /auth/token
#      GET  /auth/me
#
# See ASSESSMENT.md.
