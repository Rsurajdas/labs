from pydantic import BaseModel, ConfigDict, Field


# GIVEN
class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
