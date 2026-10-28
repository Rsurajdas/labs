from fastapi import APIRouter, HTTPException, Path
from starlette import status

from database import DB_DEPENDENCY
from models.auth import User
from schemas.auth import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def find_user(db: DB_DEPENDENCY, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


@router.get("/users/{id}", response_model=UserResponse)
async def get_user_by_id(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    user = find_user(db, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
