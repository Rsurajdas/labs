import bcrypt
from fastapi import APIRouter, HTTPException, Path
from starlette import status

from database import DB_DEPENDENCY
from models.auth import User
from schemas.auth import UserCreate, UserListResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def find_user(db: DB_DEPENDENCY, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()


@router.get("/user/", response_model=UserListResponse)
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
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed,
    )
    db.add(new_user)
    db.commit()
    return new_user


# response_model should be UserResponse
#
