from fastapi import FastAPI
from data import *

app = FastAPI()

@app.get("/books")
async def first_api():
    return {"status": "Success", "data": BOOKS}