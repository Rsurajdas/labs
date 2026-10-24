from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import DB_DEPENDENCY
from schemas import auth as auth_schema
from models import auth as auth_model
import bcrypt
from jose import JWTError, jwt

router = APIRouter()

SECRET_KEY = "a1ede91fecc536651b2ef78950e55d715a0858d53eb7241d529794f33103f4c6"
ALGORIHM = "HS256"
oauth2_beater = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_hashed_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def authenticate_user(
    password: str,
    db: DB_DEPENDENCY,
    username: str | None = None,
    email: str | None = None,
):
    if bool(username) == bool(email):
        return False

    if username:
        condition = auth_model.User.username == username
    else:
        condition = auth_model.User.email == email

    user = (
        db.query(auth_model.User)
        .filter(condition, auth_model.User.is_active == True)
        .first()
    )

    if user is None:
        return None
    if not verify_hashed_password(password, user.hashed_password):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORIHM)


def decode_jwt(token: Annotated[str, Depends(oauth2_beater)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORIHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Token is invalid!")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid!")


@router.get("/users", response_model=auth_schema.UserListResponse)
async def get_all_user(db: DB_DEPENDENCY):
    users = db.query(auth_model.User).all()
    return {
        "status": "success",
        "length": len(users),
        "data": users,
    }


@router.post("/auth/register", response_model=auth_schema.AuthResponse)
async def register(db: DB_DEPENDENCY, body: auth_schema.UserRequest):
    new_user = auth_model.User(
        email=body.email,
        username=body.username,
        first_name=body.first_name,
        last_name=body.last_name,
        role=body.role,
        hashed_password=hash_password(body.password),
        is_active=body.is_active or True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "message": "User added successfully!"}


@router.post("/auth/login", response_model=auth_schema.AuthResponse)
async def login(db: DB_DEPENDENCY, body: auth_schema.LoginRequest):
    """This approach uses a custom Pydantic request model"""
    user = authenticate_user(body.password, db, None, body.email)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Please provide valid email or password"
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {
        "status": "success",
        "message": "User logged in successfully!",
        "token": token,
    }


@router.post("/auth/sign_in", response_model=auth_schema.AuthResponse)
async def sign_in(
    formdata: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEPENDENCY
):
    user = authenticate_user(formdata.password, db, formdata.username, None)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Please provide valid email or password"
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {
        "status": "success",
        "message": "User logged in successfully!",
        "token": token,
    }
