from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool | None = Field(default=True)


class UserListResponse(BaseModel):
    count: int
    data: list[UserResponse]


class Token(BaseModel):
    access_token: str
    token_type: str
