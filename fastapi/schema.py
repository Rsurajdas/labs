from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = None
    author: str = Field(min_length=3)
    rating: int = Field(ge=1, le=5)
    
class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    title: str
    description: str
    author: str
    rating: int
    
    model_config=ConfigDict(from_attributes=True)
    
class BookResponseWrapper(BaseModel):
    status: str
    data: BookResponse