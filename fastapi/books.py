from fastapi import FastAPI
from data import *

app = FastAPI()

@app.get("/books")
async def get_all_books():
    return {"status": "Success", "data": BOOKS}

@app.get("/books/{id}")
async def get_book_by_id(id: int):
    for book in BOOKS:
        if book.get("id") == id:
            return {"status": "Success", "data": book}
        
    return {"status": "Failed", "message": "Book not found!"}