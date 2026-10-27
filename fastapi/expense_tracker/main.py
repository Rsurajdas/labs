from fastapi import FastAPI
from routers import auth, categories, expense

app = FastAPI()
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expense.router)
