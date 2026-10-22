from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: str | None = None
    role: str


class UserRequest(UserBase):
    pass


class UserReponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
