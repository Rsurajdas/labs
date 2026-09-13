from fastapi import FastAPI, Body
from data import *

app = FastAPI()

@app.get("/books")
async def get_all_books(in_stock: bool | None=None):
    if in_stock == None:
        return {"status": "success", "results": len(BOOKS), "data": BOOKS}
    result = []
    for book in BOOKS:
        if book.get("in_stock") == in_stock:
            result.append(book)
        
    return {"status": "success", "results": len(result), "data": result}

@app.get("/books/{id}")
async def get_book_by_id(id: int):
    for book in BOOKS:
        if book.get("id") == id:
            return {"status": "success", "data": book}
        
    return {"status": "failed", "message": "Book not found!"}

@app.post("/books")
async def create_book(book=Body()):
    if not book.get("id"):
        return {"status": "failed", "message": "Books must have a unique `id`"}
    if not book.get("title"):
        return {"status": "failed", "message": "Books must have a `title`"}

    BOOKS.append(book)
    return {"status": "success", "data": book, "message": "Book successfully added"}

@app.put("/books/{id}")
async def update_book_by_id(id: int, body=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == id:
            BOOKS[i] = body
            return {"status": "success", "message": "Book updated successfully"}
        
    return {"status": "failed", "message": "Book not found!"}

    