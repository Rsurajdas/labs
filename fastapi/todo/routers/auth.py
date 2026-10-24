from fastapi import APIRouter, HTTPException
from database import DB_DEPENDENCY
from schemas import auth as auth_schema
from models import auth as auth_model
import bcrypt

router = APIRouter()


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_hashed_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


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


@router.post("/auth/login")
async def login(db: DB_DEPENDENCY, body: auth_schema.LoginRequest):
    user = db.query(auth_model.User).filter_by(email=body.email).first()
    if user is None or not verify_hashed_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Please provide valid email or password"
        )
    if not user.is_valid:
        raise HTTPException(status_code=401, detail="User account is inactive")
    return {"status": "success", "message": "User logged in successfully!"}
