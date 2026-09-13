from fastapi import FastAPI, Body
from data import *

app = FastAPI()

@app.get("/books")
async def get_all_books(in_stock: bool):
    result = []
    for book in BOOKS:
        if book.get("in_stock") == in_stock:
            result.append(book)
        
    return {"status": "Success", "results": len(result), "data": result}

@app.get("/books/{id}")
async def get_book_by_id(id: int):
    for book in BOOKS:
        if book.get("id") == id:
            return {"status": "Success", "data": book}
        
    return {"status": "Failed", "message": "Book not found!"}

@app.post("/books")
async def create_book(book=Body()):
    if not book.get("id"):
        return {"status": "Fialed", "message": "Books must have a unique `id`"}
    if not book.get("title"):
        return {"status": "Fialed", "message": "Books must have a `title`"}

    BOOKS.append(book)
    return {"status": "Success", "data": book, "message": "Book successfully added"}

    