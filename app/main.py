from fastapi import FastAPI
from sqlmodel import SQLModel

from app.presistence.models import Building, Expense_User, Expense, ExpenseItem, Flat, Property, User
from .config import createDbAndTables
from app.presentation.userController import router as userRouter
from app.presentation.buildingController import router as buildingRouter
from app.presentation.flatController import router as flatRouter

def lifespan(app: FastAPI):
    print("Starting Vecinet")
    createDbAndTables()
    yield
    print("Shuting down Vecinet")

app = FastAPI(lifespan=lifespan)

app.include_router(userRouter, prefix="/users", tags=["Users"])
app.include_router(buildingRouter, prefix="/buildings", tags=["Buildings"])
app.include_router(flatRouter, prefix="/flats", tags=["Flats"])

