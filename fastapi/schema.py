from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = None
    author: str = Field(min_length=3)
    rating: int = Field(ge=1, le=5)
    published_date: int | None = None
    
    model_config = ConfigDict(json_schema_extra={"example": {"title": "A new book", "description": "Book description", "author": "John doe","rating": 5,"published_date": 2023}})
    
class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    title: str
    description: str
    author: str
    rating: int
    published_date: int
    
    model_config=ConfigDict(from_attributes=True)
    
class BookResponseWrapper(BaseModel):
    status: str
    data: BookResponse