from typing import Annotated
from starlette import status

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import settings
from database import DB_DEPENDENCY
from models.user import User

# GIVEN
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB_DEPENDENCY):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        username = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")
        if username is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).filter(User.id == user_id).first()

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return user


AdminUser = Annotated[User, Depends(require_admin)]
