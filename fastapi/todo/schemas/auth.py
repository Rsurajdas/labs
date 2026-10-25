from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str | None = None
    is_active: bool | None = None
    role: str


class UserRequest(UserBase):
    pass


class LoginRequest(BaseModel):
    email: str
    password: str


class UserReponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    status: str
    length: int
    data: list[UserReponse]


class AuthResponse(BaseModel):
    status: str
    message: str
    token: str
