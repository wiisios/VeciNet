from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .expense import Expense

class ExpenseItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    cost: float
    invoiceImg: str

    expenseId: int | None = Field(default=None, foreign_key="expense.id")
    expense: "Expense" = Relationship(back_populates="items")