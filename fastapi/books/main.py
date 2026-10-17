from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Path, Query, HTTPException

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


@app.get("/books", response_model=schema.BookResponseWrapper)
async def get_all_books(
    db: DB_DEPENDENCY, rating: int | None = Query(default=None, gt=0, lt=6)
):
    books = (
        db.query(models.Books).filter_by(rating=rating).all()
        if rating
        else db.query(models.Books).all()
    )
    return {"status": "success", "length": len(books), "data": books}


@app.post("/books", response_model=schema.BookResponseWrapper)
async def create_book(book: schema.BookCreate, db: DB_DEPENDENCY):
    db_book = models.Books(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"status": "success", "data": db_book}


@app.get("/books/{id}", response_model=schema.BookResponseWrapper)
async def get_book_by_id(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    book = db.query(models.Books).filter_by(id=id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    return {"status": "success", "data": book}


@app.get("/books/published/{year}", response_model=schema.BookResponseWrapper)
async def get_books_by_published_year(year: int, db: DB_DEPENDENCY):
    books = db.query(models.Books).filter_by(published_date=year).all()
    return {"status": "success", "length": len(books), "data": books}


# Assessment #01 Q9
@app.get("/books", response_model=list[schema.BookResponse])
def get_books(
    published_after: int | None = Query(default=None),
    min_rating: float | None = Query(default=None, ge=0, le=5),
    db: Session = Depends(get_db),
):
    query = db.query(models.Books)
    if published_after is not None:
        query = query.filter(models.Books.published_date > published_after)
    if min_rating is not None:
        query = query.filter(models.Books.rating >= min_rating)
    return query.order_by(models.Books.published_date.desc()).all()
