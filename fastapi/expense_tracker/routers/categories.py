from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from database import DB_DEPENDENCY
from models.categories import Category
from schemas.categories import CategoryCreate, CategoryResponse, CategoryListResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(db: DB_DEPENDENCY, body: CategoryCreate):
    new_category = Category(**body.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=CategoryListResponse, status_code=status.HTTP_200_OK)
async def get_all_categories(db: DB_DEPENDENCY):
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return {"data": categories}


def find_category(db: DB_DEPENDENCY, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


@router.get(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def get_category_by_id(
    db: DB_DEPENDENCY, category_id: Annotated[int, Path(gt=0)]
):
    category = find_category(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!"
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(
    db: DB_DEPENDENCY, category_id: Annotated[int, Path(gt=0)]
):
    category = find_category(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!"
        )
    db.delete(category)
    db.commit()
