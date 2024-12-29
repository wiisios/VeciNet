from fastapi import FastAPI
from sqlmodel import SQLModel

from app.presistence.models import Building, Expense_User, Expense, ExpenseItem, Flat, Property, User
from .config import createDbAndTables
from app.presentation.userController import router as userRouter

def lifespan(app: FastAPI):
    print("Starting Vecinet")
    createDbAndTables()
    yield
    print("Shuting down Vecinet")

app = FastAPI(lifespan=lifespan)

app.include_router(userRouter)

