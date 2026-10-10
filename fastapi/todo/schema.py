from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = Field(min_length=3, max_length=280)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class TodoRequest(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int
    title: str
    description: str
    priority: int
    complete: bool

    model_config = ConfigDict(from_attributes=True)


class TodoResponseWrapper(BaseModel):
    status: str
    message: str | None = None
    data: list[TodoResponse] | TodoResponse | None = None
