from fastapi import FastAPI
from routers import auth, categories, expenses

app = FastAPI()
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)
