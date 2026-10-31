from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status

from database import DB_DEPENDENCY
from models.expenses import Expense
from routers.auth import find_user
from routers.categories import find_category
from schemas.expenses import (
    ExpenseCreate,
    ExpenseListResponse,
    ExpenseOut,
    ExpenseResponse,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=ExpenseListResponse)
async def get_all_expenses(
    db: DB_DEPENDENCY,
    user_id: int | None = Query(gt=0, default=None),
    category_id: int | None = Query(gt=0, default=None),
    min_amount: int | None = Query(gt=0, default=None),
):
    query = db.query(Expense)

    if user_id is not None:
        query = query.filter(Expense.user_id == user_id)
    if category_id is not None:
        query = query.filter(Expense.category_id == category_id)
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)

    expenses = query.order_by(Expense.spent_on.desc()).all()
    return {"count": len(expenses), "data": expenses}


def _find_expense(db: DB_DEPENDENCY, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()


def check_references(db, body: ExpenseCreate):
    if body.category_id is not None and find_category(db, body.category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if find_user(db, body.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{expense_id}", response_model=ExpenseOut)
async def get_expense_by_id(db: DB_DEPENDENCY, expense_id: Annotated[int, Path(gt=0)]):
    expense = _find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    return expense


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(db: DB_DEPENDENCY, body: ExpenseCreate):
    check_references(db, body)
    new_expense = Expense(**body.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    db: DB_DEPENDENCY, body: ExpenseCreate, expense_id: Annotated[int, Path(gt=0)]
):
    expense = _find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    check_references(db, body)
    for field, value in body.model_dump().items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(db: DB_DEPENDENCY, expense_id: Annotated[int, Path(gt=0)]):
    expense = _find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    db.delete(expense)
    db.commit()


#  Q11
# 1. Status code = 200
# JSON body
# {
#   "id": 3,
#   "title": "Electricity bill",
#   "amount": 1840.5,
#   "category_id": 3
# }
#
# 2. Status code = 200
# JSON body
# {
#   "id": 6,
#   "title": "Misc cash",
#   "amount": 100,
#   "category_id": 3
# }
#
# 3. Status code = 422
# JSON body
# {
#   "detail": [
#     {
#       "type": "greater_than",
#       "loc": [
#         "path",
#         "expense_id"
#       ],
#       "msg": "Input should be greater than 0",
#       "input": "0",
#       "ctx": {
#         "gt": 0
#       }
#     }
#   ]
# }
#
# 4. Status code = 204
# JSON body
# null
#
# 5. Status code = 404
# JSON body
# {
#   "detail": "Expense not found"
# }
#
# 6. Status code = 422
# JSON body
# {
#   "detail": [
#     {
#       "type": "greater_than",
#       "loc": [
#         "path",
#         "expense_id"
#       ],
#       "msg": "Input should be greater than 0",
#       "input": "0",
#       "ctx": {
#         "gt": 0
#       }
#     }
#   ]
# }
