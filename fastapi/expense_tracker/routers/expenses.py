from fastapi import APIRouter, Query

from database import DB_DEPENDENCY
from models.expenses import Expense
from schemas.expenses import ExpenseListResponse

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
