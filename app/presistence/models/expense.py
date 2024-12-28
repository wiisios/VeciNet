from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from .expense_user import Expense_User
if TYPE_CHECKING:
    from .user import User
    from .expenseItem import ExpenseItem

class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: datetime
    totalCost: float

    users: List["User"] = Relationship(back_populates="expenses", link_model=Expense_User)

    items: List["ExpenseItem"] = Relationship(back_populates="expense")