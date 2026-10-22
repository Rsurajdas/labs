from turtle import title

from fastapi import APIRouter
from database import get_db, DB_DEPENDENCY
from schemas import auth as auth_schema
from models import auth as auth_model

router = APIRouter()


@router.get("/auth/")
async def create_user(db: DB_DEPENDENCY, body: auth_schema.UserRequest):
    new_user = auth_model.User(
        email=body.email,
        username=body.username,
        first_name=body.first_name,
        last_name=body.last_name,
        role=body.role,
        hashed_password=body.password,
        is_active=body.is_active or True,
    )
    db.add(new_user)
    db.commit()
    db.refresh()
    return "User added successfully!"
