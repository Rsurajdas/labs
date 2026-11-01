from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(max_length=200, default=None)


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    model_config = ConfigDict(from_attributes=True)


class CategoryListResponse(BaseModel):
    data: list[CategoryResponse]
    model_config = ConfigDict(from_attributes=True)
