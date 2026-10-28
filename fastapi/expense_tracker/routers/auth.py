from fastapi import APIRouter, HTTPException, Path
from starlette import status

from database import DB_DEPENDENCY
from models.auth import User
from schemas.auth import UserResponse

router = APIRouter("/auth", tags=["auth"])


@router.get("/users/{id}", response_model=UserResponse)
async def get_user_by_id(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    return user
