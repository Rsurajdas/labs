from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from database import SessionLocal, engine
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: DB_DEPENDENCY):
    return db.query(models.Todo).all()


@app.get("/todos/{id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    book = db.query(models.Todo).filter(models.Todo.id == id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail="Todo not found")
