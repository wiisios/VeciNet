from fastapi import FastAPI
from sqlmodel import SQLModel

from app.persistence.models import Building, ExpenseUser, Expense, ExpenseItem, Flat, Property, User
from .config import create_db_and_tables
from app.presentation.user_controller import router as userRouter
from app.presentation.building_controller import router as buildingRouter
from app.presentation.flat_controller import router as flatRouter
from app.presentation.expense_controller import router as expenseRouter
from app.presentation.expense_item_controller import router as expenseItemRouter

def lifespan(app: FastAPI):
    print("Starting Vecinet")
    create_db_and_tables()
    yield
    print("Shuting down Vecinet")

app = FastAPI(lifespan=lifespan)

# List of routers
app.include_router(userRouter)
app.include_router(buildingRouter)
app.include_router(flatRouter)
app.include_router(expenseRouter)
app.include_router(expenseItemRouter)

