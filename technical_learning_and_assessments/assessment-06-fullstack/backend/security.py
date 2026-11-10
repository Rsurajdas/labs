from datetime import datetime, timedelta, timezone

from bcrypt import hashpw, gensalt, checkpw
from jose import jwt

from config import settings


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
) -> str:
    payload = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})
    return jwt.encode(payload, settings.secret_key, settings.algorithm)
