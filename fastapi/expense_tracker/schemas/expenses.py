from datetime import date

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    amount: float = Field(gt=0)
    spent_on: date
    category_id: int | None = Field(default=None, gt=0)
    user_id: int = Field(gt=0)


class ExpenseResponse(ExpenseCreate):
    id: int


class ExpenseListResponse(BaseModel):
    count: int
    data: list[ExpenseResponse]


# Q -> 03
# Body(A) -> This request will pass on validation
# Body(B) -> The request will fail with a 422 Unprocessable Entity error because the amount must be greater than 0
# Body(C) -> The request will fail with a 422 Unprocessable Entity error because the title must be 3 character long
# Body(D) -> This request will pass on validation
# Body(E) -> The request will fail with a 422 Unprocessable Entity error because spent_on is missing
