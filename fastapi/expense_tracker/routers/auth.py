from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status

from database import DB_DEPENDENCY
from models.auth import User
from schemas.auth import Token, UserCreate, UserListResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Secret key used to sign and verify JWT tokens.
# Keep this value secure and store it in environment variables.
SECRET_KEY = "0ec67f03f963dc09cb8516f25656bbb3512a90babca440ac9fab3f84b8ae631a"

# Algorithm used for signing and verifying JWT tokens.
ALGORITHM = "HS256"

# OAuth2 scheme for extracting the Bearer token from incoming requests.
# The tokenUrl points to the authentication endpoint used to obtain access tokens.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/sign_in")


def find_user(db: DB_DEPENDENCY, user_id: int) -> User | None:
    """
    Retrieve an active user by their ID.

    Args:
        db: Database session dependency.
        user_id: Unique identifier of the user.

    Returns:
        User | None: The matching active user if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()


def create_hashed_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_hashed_password(plain_password: str, hashed_password: str):
    """
    Verify a plain-text password against its hashed version.

    Args:
        plain_password: The plain-text password provided by the user.
        hashed_password: The stored bcrypt-hashed password.

    Returns:
        bool: True if the password matches the hash, otherwise False.
    """
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
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


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


# authenticate_user function

# 1. Add a user existence check after the database query. Otherwise, `verify_hashed_password()` may throw an error if the user is not found.
# 2. The argument order in `bcrypt.checkpw()` is incorrect. It expects the plain password first and the hashed password second.

# sign_in function

# 1. The type of `form_data` is incorrect. It should be `Annotated[OAuth2PasswordRequestForm, Depends()]`.
# 2. The wrong argument is passed to `authenticate_user()`. It expects `username`, but `email` is being passed.
# 3. The HTTPException status code is incorrect. It should be `401 (Unauthorized)`.
