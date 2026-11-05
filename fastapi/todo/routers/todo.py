from pickle import NONE
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from models import todo as todo_model
from database import DB_DEPENDENCY
from starlette import status
from schemas import todo as todo_schema
from .auth import decode_jwt

router = APIRouter(prefix="/todos", tags=["todo"])

USER_DEPENDENCY = Annotated[dict, Depends(decode_jwt)]


@router.get(
    "/",
    response_model=todo_schema.TodoListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_todos(db: DB_DEPENDENCY):
    books = db.query(todo_model.Todo).all()
    return {
        "status": "success",
        "length": len(books),
        "data": books,
    }


@router.get(
    "/{id}",
    response_model=todo_schema.TodoSingleResponse,
    status_code=status.HTTP_200_OK,
)
async def get_todo_by_id(db: DB_DEPENDENCY, id: Annotated[int, Path(gt=0)]):
    todo = db.query(todo_model.Todo).filter(todo_model.Todo.id == id).first()
    if todo is not None:
        return {
            "status": "success",
            "data": todo,
        }
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/", response_model=todo_schema.TodoSingleResponse)
async def create_todo(
    user: USER_DEPENDENCY, db: DB_DEPENDENCY, body: todo_schema.TodoRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authetication failed"
        )
    new_todo = todo_model.Todo(**body.model_dump(), owner_id=user.get("id"))

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {
        "status": "success",
        "message": "Todo is created successfully!",
        "data": new_todo,
    }


@router.put("/{id}", response_model=todo_schema.TodoSingleResponse)
async def update_todo(
    user: USER_DEPENDENCY,
    db: DB_DEPENDENCY,
    body: todo_schema.TodoRequest,
    id: Annotated[int, Path(gt=0)],
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authetication failed"
        )

    todo = db.query(todo_model.Todo).filter(todo_model.Todo.id == id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = body.title
    todo.description = body.description
    todo.priority = body.priority
    todo.complete = body.complete

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return {
        "status": "success",
        "message": "Todo is updated successfully!",
        "data": todo,
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: USER_DEPENDENCY, db: DB_DEPENDENCY, id: Annotated[int, Path(gt=0)]
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authetication failed"
        )
    todo = db.query(todo_model.Todo).filter(todo_model.Todo.id == id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(todo_model.Todo).filter(todo_model.Todo.id == id).delete()

    db.commit()
