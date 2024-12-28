from fastapi import FastAPI
from sqlmodel import SQLModel

from app.presistence.models import Building, Expense_User, Expense, ExpenseItem, Flat, User
from .config import createDbAndTables

def lifespan(app: FastAPI):
    print("Starting Vecinet")
    createDbAndTables()
    yield
    print("Shuting down Vecinet")

app = FastAPI(lifespan=lifespan)