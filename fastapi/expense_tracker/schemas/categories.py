from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(max_length=200)


class CategoryResponse(CategoryCreate):
    id: int


class CategoryListResponse(BaseModel):
    data: list[CategoryResponse]
