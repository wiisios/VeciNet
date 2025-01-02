import decimal
from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from .expense_user import ExpenseUser
if TYPE_CHECKING:
    from .user import User
    from .expense_item import ExpenseItem

class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: datetime
    total_cost: float

    users: List["User"] = Relationship(back_populates="expenses", link_model=ExpenseUser)

    items: List["ExpenseItem"] = Relationship(back_populates="expense")