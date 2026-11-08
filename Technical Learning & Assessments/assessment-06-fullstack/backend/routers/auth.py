from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from database import DB_DEPENDENCY
from models.user import User
from schemas.auth import Token, UserCreate, UserOut
from security import create_access_token, hash_password, verify_password

from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(db: DB_DEPENDENCY, username: str, password: str):
    user = (
        db.query(User)
        .filter(User.is_active == True)
        .filter(User.username == username)
        .first()
    )

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        None

    return user


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
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

    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(body.password),
        role="user",
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/token", response_model=Token)
async def sign_in(
    formdata: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEPENDENCY
):
    user = authenticate_user(db, formdata.username, formdata.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers=["WWW-Authenticate", "Bearer"],
        )

    token = create_access_token(
        user.username,
        user.id,
        user.role,
        expires_delta=settings.access_token_expire_minutes,
    )

    return {"access_token": token, "token_type": "bearer"}


#
# Q4 — authenticate_user(db, username, password)
#      POST /auth/token
#      GET  /auth/me
#
# See ASSESSMENT.md.
