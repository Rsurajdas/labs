from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)


class UserResponse(UserCreate):
    id: int
    password: None
    is_active: bool | None = Field(default=True)


class Token(BaseModel):
    access_token: str
    token_type: str
