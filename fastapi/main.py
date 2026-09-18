from typing import Annotated 
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
from models import Books
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
async def get_all_books(db: DB_DEPENDENCY):
    books = db.query(Books).all()
    return {
        "status": "success",
        "length": len(books),
        "data": books
    }