from fastapi import FastAPI
from routers import auth, category, expense

app = FastAPI()
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(expense.router)
