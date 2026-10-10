from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from database import SessionLocal, engine
from starlette import status
from schema import (
    TodoListResponse,
    TodoRequest,
    TodoSingleResponse,
)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@app.get("/todos", response_model=TodoListResponse, status_code=status.HTTP_200_OK)
async def get_all_todos(db: DB_DEPENDENCY):
    books = db.query(models.Todo).all()
    return {
        "status": "success",
        "length": len(books),
        "data": books,
    }


@app.get(
    "/todos/{id}", response_model=TodoSingleResponse, status_code=status.HTTP_200_OK
)
async def get_todo_by_id(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo is not None:
        return {
            "status": "success",
            "data": todo,
        }
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", response_model=TodoSingleResponse)
async def create_todo(db: DB_DEPENDENCY, body: TodoRequest):
    new_todo = models.Todo(**body.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {
        "status": "success",
        "message": "Todo is created successfully!",
        "data": new_todo,
    }


@app.put("/todos/{id}", response_model=TodoSingleResponse)
async def update_todo(db: DB_DEPENDENCY, body: TodoRequest, id: int = Path(gt=0)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

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
