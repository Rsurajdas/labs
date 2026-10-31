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


def find_expense(db: DB_DEPENDENCY, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()


@router.get("/{expense_id}", response_model=ExpenseOut)
async def get_expense_by_id(db: DB_DEPENDENCY, expense_id: Annotated[int, Path(gt=0)]):
    expense = find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    return expense


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(db: DB_DEPENDENCY, body: ExpenseCreate):
    category = find_category(db, body.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    user = find_user(db, body.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    new_expense = Expense(**body.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense_by_id(
    db: DB_DEPENDENCY, body: ExpenseCreate, expense_id: Annotated[int, Path(gt=0)]
):
    category = find_category(db, body.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    user = find_user(db, body.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    expense = find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    expense.title = body.title
    expense.amount = body.amount
    expense.spent_on = body.spent_on
    expense.category_id = body.category_id
    expense.user_id = body.user_id

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}")
async def delete_expense_by_id(
    db: DB_DEPENDENCY, expense_id: Annotated[int, Path(gt=0)]
):
    expense = find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    db.delete(expense)
    db.commit()
