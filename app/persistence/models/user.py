from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from .expense_user import ExpenseUser
if TYPE_CHECKING:
    from .expense import Expense
    from .flat import Flat
    from .property import Property

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    last_name: str = Field(index=True)
    password: str
    email: EmailStr = Field(index=True)
    role: str = Field(default="tenant")

    properties: List["Property"] = Relationship(back_populates="owner")
    flat_tenant: List["Flat"] = Relationship(back_populates="tenant")

    expenses: List["Expense"] = Relationship(back_populates="users", link_model=ExpenseUser)


