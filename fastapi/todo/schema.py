from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = Field(default=None, min_length=3, max_length=280)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class TodoRequest(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TodoSingleResponse(BaseModel):
    status: str
    message: str | None = None
    data: TodoResponse


class TodoListResponse(BaseModel):
    status: str
    length: int
    data: list[TodoResponse]
