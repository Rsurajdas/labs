from typing import Annotated 
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Path, Query

import models
import schema

from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]

@app.get("/books")
async def get_all_books(db: DB_DEPENDENCY, rating: int | None = Query(default=None, gt=0, lt=6)):
    if rating:
        books = db.query(models.Books).filter_by(rating=rating).all()
    else:
        books = db.query(models.Books).all()
    return {
        "status": "success",
        "length": len(books),
        "data": books
    }
    
@app.post("/books", response_model=schema.BookResponseWrapper)
async def create_book(book: schema.BookCreate, db: DB_DEPENDENCY):
    db_book = models.Books(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {
        "status": "success",
        "data": db_book
    }

@app.get("/books/{id}")
async def get_book_by_id( db: DB_DEPENDENCY, id: int = Path(gt=0)):
    book = db.query(models.Books).filter_by(id=id).first()
    return {
        "status": "success",
        "data": book
    }

@app.get("/books/published/{year}")
async def get_books_by_published_year(year: int, db: DB_DEPENDENCY):
    books = db.query(models.Books).filter_by(published_date=year).all()
    return {
        "status": "success",
        "length": len(books),
        "data": books
    }