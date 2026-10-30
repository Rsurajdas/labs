from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status

from database import DB_DEPENDENCY
from models.auth import User
from schemas.auth import Token, UserCreate, UserListResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "0ec67f03f963dc09cb8516f25656bbb3512a90babca440ac9fab3f84b8ae631a"


def find_user(db: DB_DEPENDENCY, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()


def create_hashed_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_hashed_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return None
    if not verify_hashed_password(password, user.hashed_password):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm="HS256")


@router.get("/users/", response_model=UserListResponse)
async def get_all_users(db: DB_DEPENDENCY):
    users = db.query(User).all()
    return {"count": len(users), "data": users}


@router.get("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    user = find_user(db, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: DB_DEPENDENCY):
    hashed = create_hashed_password(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 1. The `response_model` should be `UserResponse`, not `UserCreate`.
# 2. `db.refresh(new_user)` is missing after creating the user.
# 3. Missing encoding/decoding methods: use `.decode("utf-8")` with `bcrypt.hashpw()` and `.encode("utf-8")` with `user.password`.
# 4. `is_active` is set to `False`, which means newly created users will be inactive. Set it to `True` if users should be active by default.


@router.post("/sign_in", response_model=Token)
def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEPENDENCY
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(
        user.username, user.id, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}
