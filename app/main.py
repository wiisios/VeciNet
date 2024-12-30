from fastapi import FastAPI
from sqlmodel import SQLModel

from app.presistence.models import Building, Expense_User, Expense, ExpenseItem, Flat, Property, User
from .config import createDbAndTables
from app.presentation.userController import router as userRouter
from app.presentation.buildingController import router as buildingRouter
from app.presentation.flatController import router as flatRouter
from app.presentation.expenseController import router as expenseRouter
from app.presentation.expenseItemController import router as expenseItemRouter

def lifespan(app: FastAPI):
    print("Starting Vecinet")
    createDbAndTables()
    yield
    print("Shuting down Vecinet")

app = FastAPI(lifespan=lifespan)

app.include_router(userRouter)
app.include_router(buildingRouter)
app.include_router(flatRouter)
app.include_router(expenseRouter)
app.include_router(expenseItemRouter)

