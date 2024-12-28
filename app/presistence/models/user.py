from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from .expense_user import Expense_User
if TYPE_CHECKING:
    from .expense import Expense
    from .flat import Flat

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    lastName: str = Field(index=True)
    password: str
    email: EmailStr = Field(index=True)
    isOwner: bool = Field(default=False)
    isRealEstate: bool = Field(default=False)
    title: str | None = Field(default=None)

    flatId: int | None = Field(default=None, foreign_key="flat.id")
    flatOwner: List["Flat"] = Relationship(back_populates="owner")

    flatTenantId: int | None = Field(default=None, foreign_key="flat.id")

    expenses: List["Expense"] = Relationship(back_populates="users", link_model=Expense_User)


